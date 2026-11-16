#!/usr/bin/env python3
"""Compara tu copia con el original: captura las dos a la misma anchura y te dice cuánto se parecen y DÓNDE no.

Uso:  python3 comparar.py ~/Webs/cliente/original/escritorio.png ~/Webs/cliente/copia/index.html [--ancho 1440]
      (el segundo puede ser un .html local, una URL o otra captura .png)

Deja junto a la copia:  comparacion.png  (original | copia | diferencias en rojo, franja a franja)
y escribe la similitud total y las 5 franjas de 300 px que más difieren, para arreglar esas primero.
"""
import argparse, os, sys

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

def captura(ruta, ancho, destino):
    if ruta.lower().endswith('.png'):
        return ruta
    from playwright.sync_api import sync_playwright
    url = ruta if ruta.startswith('http') else 'file://' + os.path.abspath(os.path.expanduser(ruta))
    with sync_playwright() as pw:
        b = abrir_navegador(pw); p = b.new_page(viewport={'width': ancho, 'height': 900})
        p.goto(url, wait_until='load', timeout=60000); esperar_red(p)
        p.evaluate("""async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += 600) {
            window.scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); } window.scrollTo(0, 0); }""")
        p.wait_for_timeout(600); p.screenshot(path=destino, full_page=True); b.close()
    return destino

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('original'); ap.add_argument('copia'); ap.add_argument('--ancho', type=int, default=1440)
    a = ap.parse_args()
    try:
        from PIL import Image, ImageChops
    except ImportError:
        sys.exit('Falta Pillow:  pip install pillow')
    base = os.path.dirname(os.path.abspath(os.path.expanduser(a.copia))) if not a.copia.startswith('http') else os.getcwd()
    o = Image.open(captura(os.path.expanduser(a.original), a.ancho, os.path.join(base, '_original.png'))).convert('RGB')
    c = Image.open(captura(a.copia, a.ancho, os.path.join(base, '_copia.png'))).convert('RGB')
    w = min(o.width, c.width); o = o.resize((w, round(o.height * w / o.width))); c = c.resize((w, round(c.height * w / c.width)))
    h = max(o.height, c.height)
    O = Image.new('RGB', (w, h), 'white'); O.paste(o); C = Image.new('RGB', (w, h), 'white'); C.paste(c)
    d = ImageChops.difference(O, C).convert('L')
    mask = d.point(lambda v: 255 if v > 40 else 0)
    total = sum(mask.histogram()[255:]) / (w * h)
    franjas = []
    for y in range(0, h, 300):
        caja = mask.crop((0, y, w, min(h, y + 300))); n = caja.histogram()[255] / (caja.width * caja.height)
        franjas.append((n, y))
    roja = C.copy(); roja.paste(Image.new('RGB', (w, h), (255, 0, 0)), mask=mask)
    m = Image.new('RGB', (w * 3 + 40, h), (30, 30, 30)); m.paste(O, (0, 0)); m.paste(C, (w + 20, 0)); m.paste(roja, (2 * w + 40, 0))
    esc = min(1, 3000 / m.width); m = m.resize((round(m.width * esc), round(m.height * esc)))
    salida = os.path.join(base, 'comparacion.png'); m.save(salida)
    print(f'Similitud: {100 * (1 - total):.1f} %   (alto original {o.height} px · copia {c.height} px)')
    print('Franjas que más difieren (arregla estas primero):')
    for n, y in sorted(franjas, reverse=True)[:5]:
        print(f'  y = {y:>5}–{y + 300:<5} px  → {100 * n:.0f} % distinto')
    print(f'→ {salida}')

if __name__ == '__main__':
    main()
