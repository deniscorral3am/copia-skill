# Te copio cualquier web

Así copiamos una web en minutos: captura de la página entera desde el inspector, se la pasamos a Claude con un prompt
que tenemos guardado y la monta igual. Después la mejoramos con los datos del negocio y se la enseñamos al cliente en la
primera llamada: «así quedaría tu web».

## Lo que necesitas
- Claude Code con tu cuenta de Claude.
- Python 3 con Playwright y Pillow (la skill te dice cómo instalarlos).
- La URL de la web.

## A mano, sin instalar nada
1. Abre la web en Chrome → clic derecho → **Inspeccionar**.
2. `Cmd + Shift + P` (en Windows `Ctrl + Shift + P`) → escribe **Capture full size screenshot** → Intro.
3. Arrastra la captura a Claude Code con el prompt de abajo.

## Con la skill (mejor)
| Paso | Qué hace | Archivo |
|---|---|---|
| Captura | Página entera en escritorio y móvil + tipografías, colores, tamaños y textos reales | `scripts/captura.py` |
| Replica | Claude la monta con el prompt exacto | `copia/index.html` |
| Compara | Original, copia y diferencias en rojo, con las franjas que más fallan | `scripts/comparar.py` |
| Mejora | La versión para el cliente | `mejorada/index.html` |

Con la ficha de estilo Claude no adivina la tipografía ni los colores: usa los de verdad. Y con la comparación no te
fías de «parece igual»: mide cuánto se parece y dónde no.

## El prompt exacto
```text
[captura escritorio.png] [captura movil.png] [estilo.json] [textos.md]
Replica esta web exactamente igual: estructura, tipografía, colores y espaciados.
- Un solo index.html con el CSS dentro, sin frameworks. Ancho de escritorio 1440 px y versión móvil a 390 px como en
  movil.png.
- Usa las tipografías de estilo.json (si no son libres, la de Google Fonts más parecida) con los mismos tamaños y pesos,
  y los colores exactos de estilo.json.
- Los textos, los de textos.md tal cual. Las imágenes como bloques del mismo tamaño y proporción (o las del cliente si
  me las das).
- Respeta el orden y la altura de cada bloque de la captura. No añadas nada que no esté.
Cuando acabes, compárala con scripts/comparar.py y arregla las franjas que más difieran hasta que no mejore más.
```

## La versión mejorada (para la llamada)
- Móvil primero: el 70 % de sus visitas llega desde el móvil.
- Una sola llamada a la acción clara arriba (reservar, pedir presupuesto, WhatsApp) y repetida al final.
- Velocidad: imágenes comprimidas y con tamaño, sin scripts que no sirven.
- Sus opiniones reales y sus datos de contacto bien visibles.
- SEO local básico: título, descripción, nombre del negocio y ciudad.
Nada inventado: lo que falte, como `[[pendiente]]`.

## Ojo
Copiar la estructura y el estilo para enseñar una propuesta a tu cliente está bien. Publicar la web de otra marca con
sus logos, fotos y textos, no.
