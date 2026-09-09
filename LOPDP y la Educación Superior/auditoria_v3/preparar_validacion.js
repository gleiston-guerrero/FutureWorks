/* ============================================================================
 *  PREPARAR VALIDACION MANUAL — enumera los elementos a evaluar en un sitio
 *  ---------------------------------------------------------------------------
 *  Version 1.0 (agosto 2026).
 *
 *  Para UN sitio, carga la pagina en las mismas condiciones que la auditoria
 *  automatizada y produce la lista cerrada de elementos que hay que juzgar a
 *  mano en los tres criterios de la submuestra de validacion:
 *
 *    1.1.1  Contenido no textual   -> imagenes, con su atributo alt
 *    1.4.3  Contraste minimo       -> texto, con su relacion de contraste
 *    2.4.4  Proposito del enlace   -> enlaces, con su nombre accesible
 *
 *  Aplica la regla de inspeccion del manual: hasta 25 elementos por criterio,
 *  colocando PRIMERO los que axe marco como violacion o como pendientes de
 *  revision humana, y despues el resto en orden de aparicion en el documento.
 *  Asi la lista es cerrada, reproducible y no depende de lo que a cada persona
 *  se le ocurra mirar.
 *
 *  LO QUE ESTE SCRIPT NO HACE. No emite el veredicto. Calcula lo calculable
 *  (el valor de alt, la relacion de contraste cuando el fondo es un color
 *  solido, el nombre accesible de cada enlace) y deja en blanco la columna de
 *  juicio. Cuando el fondo es una imagen o un degradado, marca la fila como
 *  NO CALCULABLE, que es justamente el caso en que hace falta el ojo humano.
 *
 *  USO (Windows, desde la carpeta del proyecto):
 *      node preparar_validacion.js --id=7
 *      node preparar_validacion.js --id=14
 *      node preparar_validacion.js --id=83
 *      node preparar_validacion.js --id=95
 *      node preparar_validacion.js --id=96
 *
 *  Requiere universidades.json en la misma carpeta, mas playwright y axe-core.
 *
 *  SALIDA, en la carpeta validacion/:
 *      <SIGLA>_elementos.csv     lista para rellenar la columna de veredicto
 *      <SIGLA>_ficha.html        la misma lista, legible, con el resumen
 *      <SIGLA>_pagina.png        captura de pagina completa como evidencia
 * ==========================================================================*/

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// --------------------------- Argumentos ------------------------------------
function arg(n, d) {
	const p = process.argv.find((a) => a.startsWith('--' + n + '='));
	return p ? p.split('=').slice(1).join('=') : d;
}
const ID = parseInt(arg('id', ''), 10);
const MAX = parseInt(arg('max', '25'), 10);

if (!ID) {
	console.error('\nERROR: falta --id.');
	console.error('       Los cinco sitios de control son: 7, 14, 83, 95 y 96.');
	console.error('       Ejemplo: node preparar_validacion.js --id=7\n');
	process.exit(1);
}

// Identicos a la auditoria automatizada. NO MODIFICAR.
const ESPERA_JS_MS = 4000;
const TIMEOUT_MS = 45000;
const USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
                   '(KHTML, like Gecko) Chrome/128.0 Safari/537.36';
const VIEWPORT = { width: 1280, height: 720 };

const axeSource = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');

// --------------------------- Extraccion en la pagina -----------------------
// Todo lo que sigue se ejecuta dentro del navegador.
function recolectar(marcados, MAX) {
	// --- utilidades -------------------------------------------------------
	const selector = (el) => {
		if (!el || el.nodeType !== 1) return '';
		if (el.id) return '#' + CSS.escape(el.id);
		const partes = [];
		let n = el;
		while (n && n.nodeType === 1 && partes.length < 5) {
			let s = n.tagName.toLowerCase();
			if (n.id) { partes.unshift('#' + CSS.escape(n.id)); break; }
			const hs = n.parentNode ? Array.from(n.parentNode.children).filter((c) => c.tagName === n.tagName) : [];
			if (hs.length > 1) s += ':nth-of-type(' + (hs.indexOf(n) + 1) + ')';
			partes.unshift(s);
			n = n.parentElement;
		}
		return partes.join(' > ');
	};

	const visible = (el) => {
		const r = el.getBoundingClientRect();
		const st = getComputedStyle(el);
		return r.width > 0 && r.height > 0 && st.visibility !== 'hidden' &&
		       st.display !== 'none' && parseFloat(st.opacity) > 0.05;
	};

	const rgb = (s) => {
		const m = (s || '').match(/rgba?\(([^)]+)\)/);
		if (!m) return null;
		const p = m[1].split(',').map((x) => parseFloat(x.trim()));
		return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
	};

	const lum = (c) => {
		const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
		return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
	};

	const contraste = (a, b) => {
		const L1 = lum(a), L2 = lum(b);
		return (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
	};

	// Fondo efectivo: sube por los ancestros hasta encontrar un color opaco.
	// Devuelve null si encuentra imagen o degradado, que es el caso indecidible.
	const fondo = (el) => {
		let n = el;
		while (n && n.nodeType === 1) {
			const st = getComputedStyle(n);
			if (st.backgroundImage && st.backgroundImage !== 'none') return { indecidible: st.backgroundImage.slice(0, 60) };
			const c = rgb(st.backgroundColor);
			if (c && c.a >= 0.95) return { color: c };
			if (c && c.a > 0.05) return { indecidible: 'fondo semitransparente ' + st.backgroundColor };
			n = n.parentElement;
		}
		return { color: { r: 255, g: 255, b: 255, a: 1 } };
	};

	const nombreAccesible = (el) => {
		const al = el.getAttribute('aria-label');
		if (al && al.trim()) return { valor: al.trim(), origen: 'aria-label' };
		const lb = el.getAttribute('aria-labelledby');
		if (lb) {
			const txt = lb.split(/\s+/).map((i) => (document.getElementById(i) || {}).innerText || '').join(' ').trim();
			if (txt) return { valor: txt, origen: 'aria-labelledby' };
		}
		const t = (el.innerText || '').trim();
		if (t) return { valor: t, origen: 'texto' };
		const img = el.querySelector('img[alt]');
		if (img && img.getAttribute('alt').trim()) return { valor: img.getAttribute('alt').trim(), origen: 'alt de imagen' };
		const ti = el.getAttribute('title');
		if (ti && ti.trim()) return { valor: ti.trim(), origen: 'title' };
		return { valor: '', origen: 'SIN NOMBRE ACCESIBLE' };
	};

	// --- 1.1.1  imagenes ---------------------------------------------------
	const imagenes = Array.from(document.querySelectorAll('img, [role="img"], svg[aria-label], input[type="image"]'))
		.filter(visible)
		.map((el) => {
			const alt = el.hasAttribute('alt') ? el.getAttribute('alt') : (el.getAttribute('aria-label') || null);
			const dentroEnlace = !!el.closest('a[href]');
			const r = el.getBoundingClientRect();
			const src0 = el.currentSrc || el.src || el.getAttribute('data-src') || '';
			return {
				criterio: '1.1.1',
				src: src0 ? new URL(src0, location.href).href : '',
				selector: selector(el),
				detalle: (el.getAttribute('src') || el.getAttribute('data-src') || '').split('/').pop().slice(0, 60),
				valor: alt === null ? 'SIN ATRIBUTO alt' : (alt === '' ? 'alt="" (decorativa)' : 'alt="' + alt.slice(0, 90) + '"'),
				contexto: dentroEnlace ? 'dentro de un enlace: el alt debe describir el DESTINO' : '',
				tamano: Math.round(r.width) + 'x' + Math.round(r.height),
				automatico: alt === null ? 'INCUMPLE (sin alt)' : 'REQUIERE JUICIO'
			};
		});

	// --- 1.4.3  texto ------------------------------------------------------
	const SEL_TXT = 'p,h1,h2,h3,h4,h5,h6,li,a,span,td,th,label,button,legend,figcaption,dt,dd,blockquote,summary';
	const textos = Array.from(document.querySelectorAll(SEL_TXT))
		.filter((el) => {
			if (!visible(el)) return false;
			const propio = Array.from(el.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim().length > 1);
			return propio;
		})
		.map((el) => {
			const st = getComputedStyle(el);
			const px = parseFloat(st.fontSize);
			const pt = px * 0.75;
			const negrita = parseInt(st.fontWeight, 10) >= 700;
			const grande = pt >= 18 || (negrita && pt >= 14);
			const umbral = grande ? 3.0 : 4.5;
			const fg = rgb(st.color);
			const bg = fondo(el);
			let medido = null, veredicto;
			if (bg.indecidible || !fg) {
				veredicto = 'NO CALCULABLE: ' + (bg.indecidible || 'color no legible');
			} else {
				medido = contraste(fg, bg.color);
				veredicto = medido >= umbral ? 'cumple auto' : 'INCUMPLE auto';
			}
			return {
				criterio: '1.4.3',
				selector: selector(el),
				detalle: (el.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 60),
				valor: medido === null ? '—' : medido.toFixed(2) + ':1  (umbral ' + umbral + ':1)',
				contexto: Math.round(pt) + 'pt' + (negrita ? ' negrita' : '') + (grande ? ' [texto grande]' : ''),
				tamano: st.color + ' sobre ' + (bg.color ? 'rgb(' + [bg.color.r, bg.color.g, bg.color.b].join(',') + ')' : 'fondo variable'),
				automatico: veredicto
			};
		});

	// --- 2.4.4  enlaces ----------------------------------------------------
	const enlaces = Array.from(document.querySelectorAll('a[href]')).filter(visible);
	const porNombre = {};
	enlaces.forEach((el) => {
		const n = nombreAccesible(el).valor.toLowerCase();
		if (!n) return;
		porNombre[n] = porNombre[n] || new Set();
		porNombre[n].add(el.getAttribute('href'));
	});
	const GENERICOS = ['leer mas', 'leer más', 'ver mas', 'ver más', 'mas informacion', 'más información',
		'clic aqui', 'clic aquí', 'aqui', 'aquí', 'read more', 'more', 'click here', 'here',
		'ver', 'detalles', 'details', 'saber mas', 'saber más', 'continuar', 'enlace', 'link', 'ir'];
	const links = enlaces.map((el) => {
		const na = nombreAccesible(el);
		const bajo = na.valor.toLowerCase().trim();
		const dup = porNombre[bajo] && porNombre[bajo].size > 1;
		let veredicto = 'REQUIERE JUICIO';
		if (!na.valor) veredicto = 'INCUMPLE (sin nombre accesible)';
		else if (GENERICOS.includes(bajo)) veredicto = 'SOSPECHOSO (texto generico)';
		else if (dup) veredicto = 'SOSPECHOSO (mismo nombre, distinto destino)';
		const padre = el.parentElement ? (el.parentElement.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 90) : '';
		return {
			criterio: '2.4.4',
			selector: selector(el),
			detalle: (el.getAttribute('href') || '').slice(0, 60),
			valor: na.valor ? '"' + na.valor.slice(0, 70) + '"' : '(vacio)',
			contexto: 'origen: ' + na.origen + (padre ? ' | contexto: ' + padre : ''),
			tamano: '',
			automatico: veredicto
		};
	});

	// --- prioridad: primero lo que axe no pudo decidir ---------------------
	const marcado = (fila) => marcados.some((m) => m && fila.selector && (m.includes(fila.selector) || fila.selector.includes(m)));
	const ordenar = (arr) => {
		const a = arr.filter(marcado), b = arr.filter((x) => !marcado(x));
		return a.concat(b);
	};

	// Se recorta aqui, y se etiqueta cada elemento conservado con data-vm,
	// para poder recortarle una captura despues desde Node.
	const marcar = (arr, pref) => {
		const out = ordenar(arr).slice(0, MAX);
		out.forEach((f, i) => {
			const el = document.querySelector(f.selector);
			const id = pref + (i + 1);
			if (el) { el.setAttribute('data-vm', id); }
			f.vm = el ? id : null;
		});
		return out;
	};

	return {
		imagenes: marcar(imagenes, 'a'),
		textos: marcar(textos, 'b'),
		enlaces: marcar(links, 'c'),
		totales: { imagenes: imagenes.length, textos: textos.length, enlaces: enlaces.length }
	};
}

// --------------------------- Salidas ---------------------------------------
const esc = (s) => {
	const v = s === undefined || s === null ? '' : String(s);
	return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v;
};

const escHtml = (s) => String(s === undefined || s === null ? '' : s)
	.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function csv(uni, bloques, ruta) {
	const cab = ['criterio', 'n', 'selector', 'detalle', 'valor_medido', 'contexto',
	             'extra', 'lectura_automatica', 'VEREDICTO_HUMANO', 'nota'];
	const filas = [cab.join(',')];
	for (const [, arr] of Object.entries(bloques)) {
		arr.forEach((f, i) => {
			filas.push([f.criterio, i + 1, f.selector, f.detalle, f.valor, f.contexto,
			            f.tamano, f.automatico, '', ''].map(esc).join(','));
		});
	}
	fs.writeFileSync(ruta, '\ufeff' + filas.join('\n'), 'utf8');
}

function html(uni, bloques, tot, ruta) {
	const seccion = (id, titulo, arr, total) => `
	<h2>${escHtml(titulo)}</h2>
	<p class="meta">Se listan <b>${arr.length}</b> elementos de <b>${total}</b> presentes en la pagina.
	   Los primeros son los que axe no pudo decidir.</p>
	<div class="tally" id="t_${id}">
		<span>n = <b>${arr.length}</b></span>
		<span>evaluados <b class="ev">0</b></span>
		<span>incumplen f = <b class="f">0</b></span>
		<span>proporcion <b class="p">—</b></span>
		<span class="cod">codigo: <b>—</b></span>
	</div>
	<table data-grupo="${id}">
		<tr><th>#</th><th>Elemento</th><th>Valor medido</th><th>Contexto</th><th>Lectura automatica</th><th style="width:190px">Su veredicto</th></tr>
		${arr.map((f, i) => `<tr class="${/INCUMPLE|SIN NOMBRE|NO CALCULABLE|SOSPECHOSO/.test(f.automatico) ? 'alerta' : ''}">
			<td>${i + 1}</td>
			<td class="el">${f.img ? `<img src="${f.img}" alt="">`
			      : (f.src ? `<img src="${escHtml(f.src)}" alt=""><span class="sinimg">imagen original (elemento oculto)</span>`
			      : '<span class="sinimg">sin recorte: elemento oculto y sin imagen asociada</span>')}
			    <br><code>${escHtml(f.selector)}</code><br><small>${escHtml(f.detalle)}</small></td>
			<td>${escHtml(f.valor)}</td>
			<td><small>${escHtml(f.contexto)} ${escHtml(f.tamano)}</small></td>
			<td>${escHtml(f.automatico)}</td>
			<td class="v">
				<button class="ok" data-v="ok">cumple</button>
				<button class="no" data-v="no">incumple</button>
				<button class="na" data-v="na">no aplica</button>
			</td></tr>`).join('')}
	</table>`;
	const doc = `<!doctype html><html lang="es"><meta charset="utf-8">
	<title>Validacion manual — ${escHtml(uni.sigla)}</title>
	<style>
	 body{font:14px/1.5 Arial,sans-serif;margin:24px;color:#222;max-width:1280px}
	 h1{color:#1F3864;margin-bottom:2px} h2{color:#1F3864;margin-top:28px;border-bottom:2px solid #1F3864;padding-bottom:3px}
	 .meta{color:#555;font-size:13px} table{border-collapse:collapse;width:100%;margin-top:8px}
	 th{background:#1F3864;color:#fff;font-size:12px;padding:6px;text-align:left}
	 td{border:1px solid #ccc;padding:5px;vertical-align:top;font-size:12px}
	 tr.alerta td{background:#FFF4E5}
	 td.el img{max-width:420px;max-height:200px;border:1px solid #999;display:block;margin-bottom:4px;background:
	   repeating-conic-gradient(#eee 0% 25%,#fff 0% 50%) 50%/12px 12px}
	 .sinimg{color:#999;font-size:11px;font-style:italic} code{font-size:11px;color:#B8860B;word-break:break-all}
	 .aviso{background:#FFF2CC;border-left:4px solid #B8860B;padding:10px;margin:14px 0}
	 .tally{background:#F2F2F2;border:2px solid #1F3864;padding:8px 10px;margin-top:10px;font-size:14px;display:flex;gap:26px;flex-wrap:wrap;
	   position:sticky;top:0;z-index:20}
	 .tally .f{color:#B8860B;font-size:17px} .tally .ev{font-size:16px}
	 .tally .cod b{font-size:16px;color:#1F3864}
	 .v button{font:12px Arial;margin:1px;padding:3px 7px;border:1px solid #aaa;background:#fff;cursor:pointer;border-radius:3px}
	 .v button.sel.ok{background:#1F3864;color:#fff;border-color:#1F3864}
	 .v button.sel.no{background:#B8860B;color:#fff;border-color:#B8860B}
	 .v button.sel.na{background:#777;color:#fff;border-color:#777}
	 #resumen{position:fixed;right:18px;bottom:18px;background:#1F3864;color:#fff;padding:12px 14px;border-radius:6px;font-size:13px;box-shadow:0 2px 10px rgba(0,0,0,.3);max-width:330px}
	 #resumen b{font-size:15px} #resumen button{margin-top:8px;font:12px Arial;padding:5px 9px;cursor:pointer;border:0;border-radius:3px;background:#fff;color:#1F3864;font-weight:bold}
	 #resumen pre{margin:6px 0 0;font:12px Consolas,monospace;white-space:pre-wrap}
	</style>
	<h1>${escHtml(uni.sigla)} — ${escHtml(uni.nombre || '')}</h1>
	<p class="meta">${escHtml(uni.url)} · generado el ${new Date().toISOString().slice(0, 16).replace('T', ' ')}
	   · ventana 1280x720, zoom 100 %, sin interaccion con banners</p>
	<div class="aviso"><b>Como se usa.</b> Pulse un boton en cada fila. El contador de cada criterio calcula solo
	   <b>n</b>, <b>f</b> y el codigo que corresponde segun el umbral del manual. <b>No aplica</b> es para las
	   excepciones legitimas, como logotipos o texto deshabilitado, y esas filas salen del denominador.
	   La columna <i>lectura automatica</i> indica donde mirar, no que concluir.
	   Nada se guarda: al terminar, copie el resumen al Excel.</div>
	${seccion('a', 'Criterio 1.1.1 — Contenido no textual (nivel A)', bloques.imagenes, tot.imagenes)}
	${seccion('b', 'Criterio 1.4.3 — Contraste minimo (nivel AA)', bloques.textos, tot.textos)}
	${seccion('c', 'Criterio 2.4.4 — Proposito del enlace en su contexto (nivel A)', bloques.enlaces, tot.enlaces)}
	<div id="resumen"><b>Resumen para el Excel</b><pre id="txt">sin evaluar</pre>
	   <button onclick="copiar()">Copiar al portapapeles</button></div>
	<script>
	var TOT = {a: ${tot.imagenes}, b: ${tot.textos}, c: ${tot.enlaces}};
	var CRIT = {a: '1.1.1', b: '1.4.3', c: '2.4.4'};
	document.querySelectorAll('table').forEach(function (tb) {
		tb.addEventListener('click', function (e) {
			var b = e.target.closest('button'); if (!b) return;
			var celda = b.parentElement;
			celda.querySelectorAll('button').forEach(function (x) { x.classList.remove('sel'); });
			b.classList.add('sel');
			recuento();
		});
	});
	function recuento() {
		var salida = [];
		['a', 'b', 'c'].forEach(function (g) {
			var tb = document.querySelector('table[data-grupo="' + g + '"]');
			var filas = tb.querySelectorAll('tr[class], tr:not(:first-child)');
			var ok = tb.querySelectorAll('button.sel.ok').length;
			var no = tb.querySelectorAll('button.sel.no').length;
			var na = tb.querySelectorAll('button.sel.na').length;
			var n = ok + no;
			var ev = ok + no + na;
			var box = document.getElementById('t_' + g);
			box.querySelector('.ev').textContent = ev;
			box.querySelector('.f').textContent = no;
			var cod = '—', prop = '—';
			if (n > 0) {
				var r = no / n;
				prop = (100 * r).toFixed(1) + ' %';
				cod = no === 0 ? '1' : (r <= 0.20 ? 'P' : '0');
			}
			box.querySelector('.p').textContent = prop;
			box.querySelector('.cod b').textContent = cod;
			salida.push(CRIT[g] + '  codigo=' + cod + '  n=' + n + ' f=' + no +
				(na ? ' (no aplica ' + na + ')' : '') + '  de ' + TOT[g] + ' en la pagina');
		});
		document.getElementById('txt').textContent = salida.join('\n');
	}
	function copiar() {
		var t = document.getElementById('txt').textContent;
		navigator.clipboard.writeText('${escHtml(uni.sigla)}\n' + t).then(function () {
			alert('Resumen copiado. Peguelo en la columna de observaciones del Excel.');
		});
	}
	recuento();
	</script>
	</html>`;
	fs.writeFileSync(ruta, doc, 'utf8');
}

// --------------------------- Programa principal ----------------------------
(async () => {
	if (!fs.existsSync('universidades.json')) {
		console.error('ERROR: falta universidades.json en esta carpeta.');
		process.exit(1);
	}
	const lista = JSON.parse(fs.readFileSync('universidades.json', 'utf8'));
	const uni = lista.find((u) => u.id === ID);
	if (!uni) {
		console.error('ERROR: no existe ninguna universidad con id=' + ID);
		process.exit(1);
	}
	if (!fs.existsSync('validacion')) fs.mkdirSync('validacion');
	const base = path.join('validacion', String(uni.sigla).replace(/[^\w-]/g, '_'));

	console.log('\n=======================================================');
	console.log(`  PREPARACION DE VALIDACION MANUAL`);
	console.log(`  ${uni.sigla} — ${uni.url}`);
	console.log('=======================================================\n');

	const browser = await chromium.launch({ headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage'] });
	const ctx = await browser.newContext({ ignoreHTTPSErrors: true, userAgent: USER_AGENT, viewport: VIEWPORT });
	const page = await ctx.newPage();

	try {
		await page.goto(uni.url, { waitUntil: 'domcontentloaded', timeout: TIMEOUT_MS });
	} catch (e) {
		console.error('FALLO al cargar: ' + String(e).split('\n')[0]);
		await browser.close();
		process.exit(2);
	}
	await page.waitForTimeout(ESPERA_JS_MS);

	// axe: solo para saber que elementos quedaron sin decidir
	await page.evaluate(axeSource);
	const ax = await page.evaluate(async () => {
		return await window.axe.run(document, {
			runOnly: { type: 'rule', values: ['image-alt', 'color-contrast', 'link-name', 'image-redundant-alt', 'link-in-text-block'] },
			resultTypes: ['violations', 'incomplete']
		});
	});
	await page.evaluate('window.__rec = ' + recolectar.toString());
	const marcados = [];
	for (const grupo of [ax.violations, ax.incomplete]) {
		for (const v of grupo) {
			for (const n of v.nodes) {
				if (n.target && n.target[0]) marcados.push(String(n.target[0]));
			}
		}
	}
	console.log(`  axe marca ${marcados.length} nodos como violacion o pendientes de revision humana.`);

	const datos = await page.evaluate(([m, mx]) => window.__rec(m, mx), [marcados, MAX]);
	const bloques = { imagenes: datos.imagenes, textos: datos.textos, enlaces: datos.enlaces };

	// --- Recorte visual de cada elemento -----------------------------------
	// Es lo que convierte la ficha en algo evaluable de un vistazo: en lugar de
	// buscar el elemento por su selector, se ve directamente.
	process.stdout.write('  Recortando capturas de cada elemento');
	let hechas = 0, fallidas = 0;
	for (const arr of [bloques.imagenes, bloques.textos, bloques.enlaces]) {
		for (const f of arr) {
			f.img = null;
			if (!f.vm) { fallidas++; continue; }
			try {
				const loc = page.locator('[data-vm="' + f.vm + '"]').first();
				await loc.scrollIntoViewIfNeeded({ timeout: 3000 }).catch(() => {});
				let b = await loc.boundingBox();
				if (!b || b.width < 2 || b.height < 2) {
					// Elemento oculto (diapositiva de carrusel, menu plegado, pestana).
					// Se fuerza su visibilidad, se recorta y se deja la pagina como estaba.
					await page.evaluate((vm) => {
						const el = document.querySelector('[data-vm="' + vm + '"]');
						if (!el) return;
						window.__prev = [];
						let n = el;
						while (n && n.nodeType === 1) {
							window.__prev.push([n, n.getAttribute('style') || '']);
							n.style.setProperty('display', 'block', 'important');
							n.style.setProperty('visibility', 'visible', 'important');
							n.style.setProperty('opacity', '1', 'important');
							n.style.setProperty('transform', 'none', 'important');
							n.style.setProperty('position', 'static', 'important');
							n.style.setProperty('max-height', 'none', 'important');
							n = n.parentElement;
						}
					}, f.vm);
					await page.waitForTimeout(120);
					await loc.scrollIntoViewIfNeeded({ timeout: 2000 }).catch(() => {});
					b = await loc.boundingBox();
					var restaurar = true;
				}
				if (!b || b.width < 2 || b.height < 2) {
					if (typeof restaurar !== 'undefined') await page.evaluate(() => {
						(window.__prev || []).forEach(([n, s]) => { if (s) n.setAttribute('style', s); else n.removeAttribute('style'); });
						window.__prev = [];
					});
					fallidas++; continue;
				}
				const clip = {
					x: Math.max(0, b.x - 4),
					y: Math.max(0, b.y - 4),
					width: Math.min(b.width + 8, 900),
					height: Math.min(b.height + 8, 320)
				};
				const buf = await page.screenshot({ clip });
				f.img = 'data:image/png;base64,' + buf.toString('base64');
				if (typeof restaurar !== 'undefined' && restaurar) await page.evaluate(() => {
					(window.__prev || []).forEach(([n, s]) => { if (s) n.setAttribute('style', s); else n.removeAttribute('style'); });
					window.__prev = [];
				});
				hechas++;
				if (hechas % 10 === 0) process.stdout.write('.');
			} catch (e) { fallidas++; }
		}
	}
	console.log(` ${hechas} capturas` + (fallidas ? `, ${fallidas} sin recorte` : ''));

	await page.screenshot({ path: base + '_pagina.png', fullPage: true }).catch(() => {});
	csv(uni, bloques, base + '_elementos.csv');
	html(uni, bloques, datos.totales, base + '_ficha.html');
	await browser.close();

	const auto = (arr, re) => arr.filter((f) => re.test(f.automatico)).length;
	console.log('');
	console.log('  Criterio  a inspeccionar / en la pagina   incumple auto   no calculable / sin nombre');
	console.log('  --------  ---------------------------   -------------   --------------------------');
	console.log(`  1.1.1     ${String(bloques.imagenes.length).padStart(3)} / ${String(datos.totales.imagenes).padEnd(20)} ${String(auto(bloques.imagenes, /INCUMPLE/)).padStart(9)}       ${auto(bloques.imagenes, /JUICIO/)} requieren juicio`);
	console.log(`  1.4.3     ${String(bloques.textos.length).padStart(3)} / ${String(datos.totales.textos).padEnd(20)} ${String(auto(bloques.textos, /INCUMPLE/)).padStart(9)}       ${auto(bloques.textos, /NO CALCULABLE/)} no calculables`);
	console.log(`  2.4.4     ${String(bloques.enlaces.length).padStart(3)} / ${String(datos.totales.enlaces).padEnd(20)} ${String(auto(bloques.enlaces, /INCUMPLE/)).padStart(9)}       ${auto(bloques.enlaces, /SOSPECHOSO/)} sospechosos`);
	console.log('');
	console.log(`  Archivos: ${base}_ficha.html   <- abra este primero`);
	console.log(`            ${base}_elementos.csv`);
	console.log(`            ${base}_pagina.png`);
	console.log('');
	console.log('  RECUERDE: la columna "lectura automatica" indica donde mirar, no que concluir.');
	console.log('  El veredicto de cada criterio y las cifras n y f los decide usted.\n');
})();
