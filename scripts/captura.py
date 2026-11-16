#!/usr/bin/env python3
"""Saca la captura de la página ENTERA de una web (escritorio y móvil) y su ficha de estilo.

Uso:  python3 captura.py https://web-del-cliente.com --salida ~/Webs/cliente/original

Deja:
  escritorio.png  página entera a 1440 px de ancho (lo mismo que «Capture full size screenshot» del inspector)
  movil.png       página entera a 390 px (iPhone)
  estilo.json     tipografías, tamaños, colores de fondo y texto más usados, anchos y textos de cada bloque
  textos.md       todos los textos visibles por orden, para no tener que leerlos de la imagen
Necesita Playwright:  pip install playwright && python3 -m playwright install chromium
"""
import argparse, collections, json, os, sys

JS = r"""() => {
  const vis = e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0.05; };
  const els = [...document.querySelectorAll('body *')].filter(vis);
  const fuentes = {}, tam = {}, fondo = {}, texto = {};
  for (const e of els) { const s = getComputedStyle(e);
    const tieneTexto = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (tieneTexto) { const f = s.fontFamily.split(',')[0].replace(/["']/g, '').trim();
      fuentes[f] = (fuentes[f] || 0) + 1; const k = s.fontSize + ' / ' + s.fontWeight; tam[k] = (tam[k] || 0) + 1;
      texto[s.color] = (texto[s.color] || 0) + 1; }
    if (s.backgroundColor && s.backgroundColor !== 'rgba(0, 0, 0, 0)') { const r = e.getBoundingClientRect();
      fondo[s.backgroundColor] = (fondo[s.backgroundColor] || 0) + Math.round(r.width * r.height / 1000); } }
  const top = (o, n) => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, n);
  const bloques = [...document.querySelectorAll('header, nav, section, footer, main > div')].filter(vis).slice(0, 40).map(e => {
    const r = e.getBoundingClientRect(); return { etiqueta: e.tagName.toLowerCase(), y: Math.round(r.top + scrollY), alto: Math.round(r.height),
      ancho: Math.round(r.width), titulo: (e.querySelector('h1,h2,h3') || {}).innerText || '' }; });
  const textos = [...document.querySelectorAll('h1,h2,h3,h4,p,li,a,button,figcaption,blockquote')].filter(vis)
    .map(e => ({ tag: e.tagName.toLowerCase(), t: e.innerText.trim().replace(/\s+/g, ' ') })).filter(x => x.t && x.t.length < 400);
  return { titulo: document.title, alto: document.documentElement.scrollHeight, fuentes: top(fuentes, 6), tamanos: top(tam, 12),
    colores_fondo: top(fondo, 8), colores_texto: top(texto, 8), bloques, textos };
}"""

def esperar_red(p):
    # espera a que la red se calme, pero sin colgarse en webs con conexiones que nunca terminan
    try:
        p.wait_for_load_state('networkidle', timeout=8000)
    except Exception:
        pass

def abrir_navegador(pw):
    # Chromium de Playwright; si no está descargado, el Google Chrome que ya tengas instalado
    try:
        return pw.chromium.launch()
    except Exception:
        try:
            return pw.chromium.launch(channel='chrome')
        except Exception:
            raise SystemExit('No encuentro navegador. Ejecuta:  python3 -m playwright install chromium')

def bajar_del_todo(p):
    # hace scroll hasta el final para que carguen las imágenes perezosas y las animaciones de entrada
    p.evaluate("""async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += 600) {
        window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } window.scrollTo(0, 0); }""")
    p.wait_for_timeout(800)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('url'); ap.add_argument('--salida', required=True)
    a = ap.parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit('Falta Playwright:  pip install playwright && python3 -m playwright install chromium\n'
                 'O hazlo a mano: Chrome → Inspeccionar → Cmd+Shift+P → «Capture full size screenshot».')
    out = os.path.expanduser(a.salida); os.makedirs(out, exist_ok=True)
    with sync_playwright() as pw:
        b = abrir_navegador(pw)
        for nombre, vp, movil in [('escritorio', {'width': 1440, 'height': 900}, False), ('movil', {'width': 390, 'height': 844}, True)]:
            p = b.new_page(viewport=vp, device_scale_factor=1 if not movil else 2, is_mobile=movil)
            p.goto(a.url, wait_until='load', timeout=60000); esperar_red(p); bajar_del_todo(p)
            p.screenshot(path=os.path.join(out, f'{nombre}.png'), full_page=True)
            if nombre == 'escritorio':
                d = p.evaluate(JS); d['url'] = a.url
                json.dump({k: v for k, v in d.items() if k != 'textos'}, open(os.path.join(out, 'estilo.json'), 'w'), ensure_ascii=False, indent=1)
                with open(os.path.join(out, 'textos.md'), 'w') as fh:
                    vistos = set()
                    for x in d['textos']:
                        if x['t'] in vistos: continue
                        vistos.add(x['t']); fh.write(('#' * int(x['tag'][1]) + ' ' if x['tag'] in ('h1', 'h2', 'h3', 'h4') else '- ' if x['tag'] in ('li', 'a', 'button') else '') + x['t'] + '\n')
            p.close()
        b.close()
    e = json.load(open(os.path.join(out, 'estilo.json')))
    print(f"✓ {out}/escritorio.png ({e['alto']} px de alto), movil.png, estilo.json, textos.md")
    print('  Tipografías:', ', '.join(f for f, _ in e['fuentes'][:3]) or '—')
    print('  Fondos:', ', '.join(c for c, _ in e['colores_fondo'][:4]) or '—')

if __name__ == '__main__':
    main()
