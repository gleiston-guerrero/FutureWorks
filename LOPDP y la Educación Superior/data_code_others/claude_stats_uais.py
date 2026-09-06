#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reanalisis estadistico del manuscrito UAIS (datos ya existentes, agosto 2026)."""
import math
import numpy as np
from scipy import stats

N = 63

# (etiqueta, exitos_mundo, exitos_ecuador)
IND = [
    ("Privacy notice published",        58, 39),
    ("Applicable framework cited",      48, 31),
    ("Data-subject rights listed",      47, 35),
    ("DPO or privacy contact",          54, 24),
    ("Declared accessibility",          47,  7),
    ("No level-A automatic failure",    25,  5),
    ("No automatic failure at all",      6,  0),
    ("Valid TLS certificate",           63, 58),
    ("Pre-consent tracking cookies",    43, 40),
    ("At least one pre-consent cookie", 56, 55),
    ("Consent banner displayed",        22, 15),
    ("CMP detected",                    12, 14),
]


def wilson(k, n, z=1.959963985):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * max(0.0, c - h), 100 * min(1.0, c + h)


def newcombe(k1, n1, k2, n2, z=1.959963985):
    """IC de la diferencia de proporciones (metodo 10 de Newcombe, score)."""
    l1, u1 = [v / 100 for v in wilson(k1, n1, z)]
    l2, u2 = [v / 100 for v in wilson(k2, n2, z)]
    d = k1 / n1 - k2 / n2
    lo = d - z * math.sqrt(l1 * (1 - l1) / n1 + u2 * (1 - u2) / n2)
    hi = d + z * math.sqrt(u1 * (1 - u1) / n1 + l2 * (1 - l2) / n2)
    return 100 * d, 100 * lo, 100 * hi


def odds_ratio(a, b, c, d):
    """a=exito mundo, b=fallo mundo, c=exito ec, d=fallo ec. Haldane-Anscombe si hay cero."""
    corr = 0.5 if 0 in (a, b, c, d) else 0.0
    A, B, C, D = a + corr, b + corr, c + corr, d + corr
    orr = (A * D) / (B * C)
    se = math.sqrt(1 / A + 1 / B + 1 / C + 1 / D)
    return orr, orr * math.exp(-1.96 * se), orr * math.exp(1.96 * se), corr > 0


print("=" * 108)
print("TABLA S1. Comparacion por indicador (n=63 por grupo). IC 95% de Wilson; "
      "diferencia por metodo de Newcombe; p de Fisher bilateral.")
print("=" * 108)
hdr = (f"{'Indicador':34s} {'Mundo % [IC95]':>24s} {'Ecuador % [IC95]':>24s} "
       f"{'Dif. pp [IC95]':>26s} {'OR [IC95]':>22s} {'p Fisher':>10s}")
print(hdr)
rows = []
pvals = []
for lab, kw, ke in IND:
    a, b, c, d = kw, N - kw, ke, N - ke
    _, p = stats.fisher_exact([[a, b], [c, d]])
    lw, uw = wilson(kw, N)
    le, ue = wilson(ke, N)
    dif, dlo, dhi = newcombe(kw, N, ke, N)
    orr, olo, ohi, corr = odds_ratio(a, b, c, d)
    pvals.append(p)
    rows.append((lab, kw, ke, lw, uw, le, ue, dif, dlo, dhi, orr, olo, ohi, p, corr))
    print(f"{lab:34s} {100*kw/N:6.1f} [{lw:5.1f},{uw:5.1f}] {100*ke/N:6.1f} [{le:5.1f},{ue:5.1f}] "
          f"{dif:+7.1f} [{dlo:+6.1f},{dhi:+6.1f}] {orr:7.2f} [{olo:5.2f},{ohi:6.2f}] {p:10.2e}")

# --- Holm-Bonferroni ---
m = len(pvals)
order = np.argsort(pvals)
adj = np.empty(m)
running = 0.0
for i, idx in enumerate(order):
    val = (m - i) * pvals[idx]
    running = max(running, val)
    adj[idx] = min(1.0, running)
print()
print("Holm-Bonferroni (m = %d comparaciones):" % m)
for (lab, *_), p, pa in zip(rows, pvals, adj):
    flag = "SIGNIFICATIVO" if pa < 0.05 else "no significativo"
    print(f"  {lab:34s} p={p:9.2e}  p_Holm={pa:9.2e}  {flag}")

# --- Equivalencia TOST para el rastreo previo al consentimiento ---
print()
print("=" * 108)
print("PRUEBA DE EQUIVALENCIA (TOST) — rastreo previo al consentimiento")
print("=" * 108)
p1, p2 = 43 / N, 40 / N
diff = p1 - p2
se = math.sqrt(p1 * (1 - p1) / N + p2 * (1 - p2) / N)
for margin in (0.10, 0.15, 0.20):
    z1 = (diff + margin) / se   # H01: dif <= -margin
    z2 = (diff - margin) / se   # H02: dif >= +margin
    pl = 1 - stats.norm.cdf(z1)
    pu = stats.norm.cdf(z2)
    ptost = max(pl, pu)
    print(f"  margen +-{margin*100:4.0f} pp -> p_TOST = {ptost:.4f}  "
          f"{'EQUIVALENCIA DEMOSTRADA' if ptost < 0.05 else 'NO se demuestra equivalencia'}")
print(f"  Diferencia observada: {100*diff:+.1f} pp; EE = {100*se:.1f} pp")
print(f"  IC 90% (el pertinente para TOST): [{100*(diff-1.645*se):+.1f}, {100*(diff+1.645*se):+.1f}] pp")
d, dlo, dhi = newcombe(43, N, 40, N)
print(f"  IC 95% Newcombe: {d:+.1f} pp [{dlo:+.1f}, {dhi:+.1f}]")

# --- Potencia del diseno ---
print()
print("POTENCIA. Diferencia minima detectable con n=63/grupo, alfa=0.05 bilateral, potencia 80%,")
pbar = (p1 + p2) / 2
za, zb = 1.959963985, 0.8416212336
mde = (za * math.sqrt(2 * pbar * (1 - pbar)) + zb * math.sqrt(2 * pbar * (1 - pbar))) / math.sqrt(N)
print(f"  partiendo de p~{pbar:.3f}: MDE = {100*mde:.1f} puntos porcentuales.")
n_needed = 2 * pbar * (1 - pbar) * (za + zb) ** 2 / (0.05 ** 2)
print(f"  Para detectar 5 pp harian falta n ~ {math.ceil(n_needed)} sitios por grupo.")
# n por grupo para equivalencia con margen 10 pp
z_a, z_b = 1.6448536, 0.8416212
n_eq = 2 * pbar * (1 - pbar) * (z_a + z_b) ** 2 / (0.10 ** 2)
print(f"  Para demostrar equivalencia con margen 10 pp (potencia 80%): n ~ {math.ceil(n_eq)} por grupo.")

# --- Spearman rho ---
print()
print("=" * 108)
print("CORRELACION accesibilidad x privacidad")
print("=" * 108)
rho, n = 0.04, 126
z = 0.5 * math.log((1 + rho) / (1 - rho))
sez = 1 / math.sqrt(n - 3)
lo = math.tanh(z - 1.96 * sez)
hi = math.tanh(z + 1.96 * sez)
t = rho * math.sqrt((n - 2) / (1 - rho ** 2))
pr = 2 * (1 - stats.t.cdf(abs(t), n - 2))
print(f"  rho = {rho:.2f}; n = {n}; IC 95% (Fisher z) = [{lo:+.3f}, {hi:+.3f}]; p = {pr:.3f}")
print(f"  Correlacion minima detectable (alfa=.05, potencia 80%, n=126): "
      f"{math.tanh((za+zb)/math.sqrt(n-3)):.3f}")
print("  -> El intervalo cubre asociaciones positivas debiles de hasta ~0.21: NO se puede afirmar independencia.")

# --- 'apenas el 3% logra ambas' ---
print()
print("Coocurrencia en Ecuador: 2/63 = %.1f%% cumplen accesibilidad nivel A y no rastrean." % (100 * 2 / 63))
p_acc, p_notrack = 5 / 63, 23 / 63
esp = 63 * p_acc * p_notrack
print(f"  Esperado bajo independencia: 63 x {p_acc:.3f} x {p_notrack:.3f} = {esp:.1f} instituciones.")
print("  -> El dato observado coincide con el azar; no sostiene ninguna tesis de acoplamiento.")

# --- Figura 4: composicionalidad y redondeo ---
print()
print("Figura de niveles (nodos con fallo): Mundo A19/AA22/AAA60 = %d ; Ecuador A45/AA29/AAA26 = %d"
      % (19 + 22 + 60, 45 + 29 + 26))
print("  -> Declarar redondeo a entero mas proximo; los porcentajes son composicionales (suman 100%).")

# --- Tabla regional: prueba global ---
print()
print("=" * 108)
print("TABLA REGIONAL: prueba global y precision")
print("=" * 108)
REG = {  # region: (n, politica, marco, dpo, accesibilidad)
    "USA": (24, 24, 18, 23, 22), "United Kingdom": (7, 6, 4, 5, 7),
    "Continental Europe": (10, 10, 9, 10, 8), "China": (6, 2, 2, 3, 0),
    "Hong Kong": (3, 3, 3, 2, 3), "Asia (others)": (5, 5, 4, 4, 0),
    "Australia": (5, 5, 5, 4, 4), "Canada": (3, 3, 3, 3, 3),
}
for j, name in enumerate(["Privacy policy", "Framework cited", "DPO", "Declared accessibility"], start=1):
    tab = [[v[j], v[0] - v[j]] for v in REG.values()]
    tab = [r for r in tab if sum(r) > 0]
    try:
        p = stats.chi2_contingency(np.array(tab).T)[1]
        method = "chi2"
    except Exception:
        p = float("nan"); method = "n/d"
    print(f"  {name:24s}  {method} p = {p:.4f}")
print()
print("  Precision por region (IC 95% Wilson, %):")
for r, v in REG.items():
    lo1, hi1 = wilson(v[1], v[0])
    print(f"    {r:20s} n={v[0]:2d}  politica {100*v[1]/v[0]:5.1f}% [{lo1:5.1f},{hi1:5.1f}]  "
          f"(semiamplitud {(hi1-lo1)/2:4.1f} pp)")
print("  -> Con n=3 la semiamplitud supera los 25 pp: las lecturas regionales no son concluyentes.")
