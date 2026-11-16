# /copia: te copio cualquier web

La skill de Claude Code que copia cualquier web (captura de la página entera + tipografías, colores y textos reales),
la replica en HTML con el prompt exacto, la compara píxel a píxel con el original y la mejora para enseñársela a tu
cliente en la primera llamada.

| Parte | Qué tienes |
|---|---|
| `scripts/captura.py` | Página entera en escritorio y móvil + ficha de estilo y textos (Playwright) |
| `scripts/comparar.py` | Similitud y franjas que más difieren, con imagen de diferencias |
| `DOCUMENTO.md` | El método, el prompt exacto y cómo hacerlo a mano desde el inspector |

Hecho por Denís Corral · [@deniscorralvillarraso](https://instagram.com/deniscorralvillarraso) · [Sell Your AI](https://sellyourai.io).

## Cómo usarlo
```bash
git clone https://github.com/deniscorral3am/copia-skill ~/.claude/skills/copia
```
Abre Claude Code y escribe `/copia`. Necesitas `pip install playwright pillow && python3 -m playwright install chromium`.

## Licencia
MIT
