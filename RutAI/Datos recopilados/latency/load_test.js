import http from "k6/http";
import ws from "k6/ws";
import { check, sleep } from "k6";
import { Trend, Rate, Counter } from "k6/metrics";

// ══════════════════════════════════════════════════════════
// CONFIGURACIÓN
// Endpoints verificados contra el backend desplegado en Render.
// Nota: el spec del paper usa nombres abreviados:
//   "POST /rutas/generar"   → implementado como POST /ml/recomendar-tipo-ruta
//   "GET /recordatorios"    → implementado como GET /reminders/listar
// ══════════════════════════════════════════════════════════
const BASE_URL = "https://recuerdago-api.onrender.com";
const WS_BASE_URL = "wss://recuerdago-api.onrender.com";

// ── CAMBIAR ESTE VALOR Y CORRER 3 VECES: 10, 50, 100 ─────
const NIVEL_CARGA = 100; // ← CAMBIAR A 10, 50 o 100

const UBICACION_OFFSET = 7;
const GRUPO_ID = 1;

// ══════════════════════════════════════════════════════════
// MÉTRICAS
// ══════════════════════════════════════════════════════════
const loginDuration = new Trend("login_duration_ms");
const rutasDuration = new Trend("rutas_generar_duration_ms");
const remindersDuration = new Trend("reminders_duration_ms");
const wsConnectDuration = new Trend("ws_connect_duration_ms");
const wsFirstMsgDuration = new Trend("ws_first_message_duration_ms");
const wsErrorCount = new Counter("ws_errors");
const errorRate = new Rate("error_rate");

// ══════════════════════════════════════════════════════════
// STAGES POR NIVEL DE CARGA
// Simula 3 "regiones geográficas" llegando en oleadas:
//   Región 1 → rampa inicial
//   Región 2 → carga sostenida
//   Región 3 → pico máximo
// ══════════════════════════════════════════════════════════
function getStages(nivel) {
  if (nivel === 10) {
    return [
      { duration: "30s", target: 3 },
      { duration: "40s", target: 3 },
      { duration: "20s", target: 7 },
      { duration: "40s", target: 7 },
      { duration: "20s", target: 10 },
      { duration: "40s", target: 10 },
      { duration: "10s", target: 0 },
    ];
  }
  if (nivel === 50) {
    return [
      { duration: "30s", target: 10 },
      { duration: "50s", target: 10 },
      { duration: "20s", target: 30 },
      { duration: "50s", target: 30 },
      { duration: "20s", target: 50 },
      { duration: "60s", target: 50 },
      { duration: "10s", target: 0 },
    ];
  }
  // 100 VUs
  return [
    { duration: "30s", target: 20 },
    { duration: "60s", target: 20 },
    { duration: "20s", target: 60 },
    { duration: "60s", target: 60 },
    { duration: "20s", target: 100 },
    { duration: "60s", target: 100 },
    { duration: "10s", target: 0 },
  ];
}

export const options = {
  setupTimeout: "300s",
  summaryTrendStats: ["avg", "min", "med", "max", "p(50)", "p(90)", "p(95)", "p(99)", "count"],
  scenarios: {
    carga_por_regiones: {
      executor: "ramping-vus",
      startVUs: 1,
      stages: getStages(NIVEL_CARGA),
    },
  },
  thresholds: {
    // Login — umbral permisivo (cold start en Render)
    "login_duration_ms": ["p(95)<60000"],

    // POST /ml/recomendar-tipo-ruta (referenciado en paper como "POST /rutas/generar")
    "rutas_generar_duration_ms": ["p(95)<5000", "p(99)<10000"],

    // GET /reminders/listar (referenciado en paper como "GET /recordatorios")
    "reminders_duration_ms": ["p(95)<3000", "p(99)<6000"],

    // WebSocket — tiempo de conexión
    "ws_connect_duration_ms": ["p(95)<5000"],

    // WebSocket — primer mensaje recibido
    "ws_first_message_duration_ms": ["p(95)<8000"],

    // Tasa de errores global < 5%
    "error_rate": ["rate<0.05"],
  },
};

// ══════════════════════════════════════════════════════════
// SETUP — login anticipado en lotes pequeños
// ══════════════════════════════════════════════════════════
export function setup() {
  const tokens = {};

  console.log("Despertando servidor...");
  let warmup;
  for (let i = 0; i < 8; i++) {
    warmup = http.get(`${BASE_URL}/health`, { timeout: "40s" });
    if (warmup.status === 200) break;
    console.log(`Intento ${i + 1}/8 — esperando...`);
    sleep(8);
  }
  console.log(`Servidor activo (status: ${warmup ? warmup.status : "?"}). Iniciando logins...`);
  sleep(5);

  const BATCH = 5;
  for (let batch = 0; batch < NIVEL_CARGA; batch += BATCH) {
    const responses = http.batch(
      Array.from({ length: Math.min(BATCH, NIVEL_CARGA - batch) }, (_, j) => {
        const i = batch + j + 1;
        return [
          "POST",
          `${BASE_URL}/login/`,
          { correo: `k6user${i}@test.com`, contrasenia: "test1234" },
          { timeout: "40s" },
        ];
      })
    );

    responses.forEach((res, j) => {
      const i = batch + j + 1;
      if (res.status === 200) {
        try {
          tokens[i] = {
            token: res.json("access_token"),
            ubicacion_id: i + UBICACION_OFFSET,
          };
        } catch (_) { tokens[i] = null; }
      } else {
        tokens[i] = null;
        console.error(`Login falló para k6user${i}: HTTP ${res.status}`);
      }
    });
    sleep(2);
  }

  const ok = Object.values(tokens).filter(Boolean).length;
  console.log(`Setup completo: ${ok}/${NIVEL_CARGA} tokens`);
  return tokens;
}

// ══════════════════════════════════════════════════════════
// FUNCIÓN PRINCIPAL
// ══════════════════════════════════════════════════════════
export default function (tokens) {
  const vuData = tokens[__VU];

  if (!vuData || !vuData.token) {
    errorRate.add(1);
    sleep(3);
    return;
  }

  const { token, ubicacion_id } = vuData;
  const headers = {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  };

  // ─── 1. Login (solo en primera iteración) ────────────
  if (__ITER === 0) {
    const loginRes = http.post(
      `${BASE_URL}/login/`,
      { correo: `k6user${__VU}@test.com`, contrasenia: "test1234" },
      { tags: { name: "login" }, timeout: "30s" }
    );
    loginDuration.add(loginRes.timings.duration);
    check(loginRes, { "login 200": (r) => r.status === 200 })
      ? errorRate.add(0) : errorRate.add(1);
    sleep(2);
  }

  // ─── 2. GET /reminders/listar ─────────────────────────
  // Paper lo referencia como "GET /recordatorios"
  const remindersRes = http.get(
    `${BASE_URL}/reminders/listar`,
    { headers, tags: { name: "GET_reminders" }, timeout: "30s" }
  );
  remindersDuration.add(remindersRes.timings.duration);
  check(remindersRes, { "reminders 200": (r) => r.status === 200 })
    ? errorRate.add(0) : errorRate.add(1);

  sleep(2);

  // ─── 3. POST /ml/recomendar-tipo-ruta ─────────────────
  // Paper lo referencia como "POST /rutas/generar"
  const rutasRes = http.post(
    `${BASE_URL}/ml/recomendar-tipo-ruta`,
    JSON.stringify({ ubicacion_id }),
    { headers, tags: { name: "POST_rutas_generar" }, timeout: "30s" }
  );
  rutasDuration.add(rutasRes.timings.duration);
  check(rutasRes, {
    "rutas 200": (r) => r.status === 200,
    "rutas tiene tipo_ruta": (r) => {
      try { return r.json("tipo_ruta") !== undefined; } catch (_) { return false; }
    },
  }) ? errorRate.add(0) : errorRate.add(1);

  sleep(2);

  // ─── 4. WebSocket /ws/{grupo_id} ──────────────────────
  testWebSocket(token);

  sleep(3);
}

// ══════════════════════════════════════════════════════════
// WEBSOCKET
// ══════════════════════════════════════════════════════════
function testWebSocket(token) {
  const wsUrl = `${WS_BASE_URL}/ws/${GRUPO_ID}?token=${token}`;
  const t0 = Date.now();

  let tiempoConectado = null;
  let tiempoMsg = null;
  let recibioBienvenida = false;
  let wsOk = false;
  let msgEnviado = false;

  const res = ws.connect(wsUrl, {}, function (socket) {
    socket.on("open", function () {
      tiempoConectado = Date.now();
      wsConnectDuration.add(tiempoConectado - t0);
      wsOk = true;
      socket.send(JSON.stringify({ action: "ping" }));
    });

    socket.on("message", function (raw) {
      if (tiempoMsg === null) {
        tiempoMsg = Date.now() - t0;
        wsFirstMsgDuration.add(tiempoMsg);
      }
      let msg;
      try { msg = JSON.parse(raw); } catch (_) { return; }

      if (msg.type === "system") recibioBienvenida = true;
      if (msg.type === "ping") socket.send(JSON.stringify({ type: "pong" }));

      if (recibioBienvenida && !msgEnviado) {
        msgEnviado = true;
        socket.send(JSON.stringify({
          action: "mensaje",
          data: {
            contenido: `k6 VU-${__VU} iter-${__ITER}`,
            tipo: "texto",
            temp_id: `k6-${__VU}-${Date.now()}`,
          },
        }));
      }
    });

    socket.on("error", function () { wsErrorCount.add(1); errorRate.add(1); });
    socket.on("close", function (code) {
      if (code !== 1000 && code !== 1001) wsErrorCount.add(1);
    });
    socket.setTimeout(function () { socket.close(); }, 8000);
  });

  check(res, {
    "ws conectó": () => wsOk,
    "ws recibió bienvenida": () => recibioBienvenida,
  }) ? errorRate.add(0) : errorRate.add(1);
}

// ══════════════════════════════════════════════════════════
// REPORTE FINAL
// ══════════════════════════════════════════════════════════
export function handleSummary(data) {
  const m = data.metrics;

  function p(name, pct) {
    const metric = m[name];
    if (!metric) return "N/A";
    const key = pct === 50 ? "med" : `p(${pct})`;
    const val = metric.values[key];
    return val !== undefined ? Math.round(val) + " ms" : "N/A";
  }
  function avg(name) {
    const metric = m[name];
    if (!metric || metric.values["avg"] === undefined) return "N/A";
    return Math.round(metric.values["avg"]) + " ms";
  }
  function cnt(name) {
    const metric = m[name];
    if (!metric) return 0;
    return metric.values["count"] ?? metric.values["value"] ?? 0;
  }
  function rate(name) {
    const metric = m[name];
    if (!metric) return "N/A";
    return (metric.values["rate"] * 100).toFixed(1) + "%";
  }
  function threshold_ok(name) {
    const metric = m[name];
    if (!metric || !metric.thresholds) return "N/A";
    const passing = Object.values(metric.thresholds).every(t => t.ok);
    return passing ? "PASS" : "FAIL";
  }

  const report = {
    nivel_usuarios: NIVEL_CARGA,
    metodologia: "ramping-vus con 3 stages (simula 3 regiones geográficas)",
    nota_endpoints: {
      "POST /ml/recomendar-tipo-ruta": "referenciado en paper como 'POST /rutas/generar'",
      "GET /reminders/listar": "referenciado en paper como 'GET /recordatorios'",
    },
    endpoints: {
      "POST /login/": {
        p50: p("login_duration_ms", 50), p95: p("login_duration_ms", 95),
        p99: p("login_duration_ms", 99), avg: avg("login_duration_ms"),
        threshold: threshold_ok("login_duration_ms"),
      },
      "POST /ml/recomendar-tipo-ruta": {
        p50: p("rutas_generar_duration_ms", 50), p95: p("rutas_generar_duration_ms", 95),
        p99: p("rutas_generar_duration_ms", 99), avg: avg("rutas_generar_duration_ms"),
        threshold: threshold_ok("rutas_generar_duration_ms"),
      },
      "GET /reminders/listar": {
        p50: p("reminders_duration_ms", 50), p95: p("reminders_duration_ms", 95),
        p99: p("reminders_duration_ms", 99), avg: avg("reminders_duration_ms"),
        threshold: threshold_ok("reminders_duration_ms"),
      },
      "WS connect time": {
        p50: p("ws_connect_duration_ms", 50), p95: p("ws_connect_duration_ms", 95),
        p99: p("ws_connect_duration_ms", 99), avg: avg("ws_connect_duration_ms"),
        threshold: threshold_ok("ws_connect_duration_ms"),
      },
      "WS first message": {
        p50: p("ws_first_message_duration_ms", 50), p95: p("ws_first_message_duration_ms", 95),
        p99: p("ws_first_message_duration_ms", 99), avg: avg("ws_first_message_duration_ms"),
        threshold: threshold_ok("ws_first_message_duration_ms"),
      },
    },
    resumen: {
      total_peticiones_http: cnt("http_reqs"),
      total_conexiones_ws: cnt("ws_sessions"),
      errores_ws: cnt("ws_errors"),
      tasa_errores: rate("error_rate"),
      threshold_error_rate: threshold_ok("error_rate"),
    },
  };

  const linea = "=".repeat(78);
  console.log(`\n${linea}`);
  console.log(`  RESULTADOS — ${NIVEL_CARGA} VUs (3 stages/regiones) — RutAI Load Test`);
  console.log(linea);
  console.log("Endpoint".padEnd(44) + "p50".padEnd(10) + "p95".padEnd(10) + "p99".padEnd(10) + "SLA");
  console.log("-".repeat(78));
  for (const [name, v] of Object.entries(report.endpoints)) {
    console.log(
      name.substring(0, 43).padEnd(44) +
      String(v.p50).padEnd(10) +
      String(v.p95).padEnd(10) +
      String(v.p99).padEnd(10) +
      (v.threshold || "N/A")
    );
  }
  console.log(linea);
  console.log(
    `HTTP reqs: ${report.resumen.total_peticiones_http}  |  ` +
    `WS: ${report.resumen.total_conexiones_ws}  |  ` +
    `Errores: ${report.resumen.tasa_errores}  |  ` +
    `SLA errores: ${report.resumen.threshold_error_rate}`
  );
  console.log(linea + "\n");

  return {
    [`resultados_${NIVEL_CARGA}vu.json`]: JSON.stringify(report, null, 2),
    stdout: JSON.stringify(report, null, 2),
  };
}