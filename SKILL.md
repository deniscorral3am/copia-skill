---
name: copia
description: Te copia cualquier web en minutos para enseñársela mejorada a tu cliente en la primera llamada. Saca la captura de la página entera (escritorio y móvil, como el inspector de Chrome) y su ficha de estilo (tipografías, colores, tamaños y textos), la replica en HTML con el prompt exacto, la compara píxel a píxel con el original y arregla las zonas que no cuadran, y después la mejora con los datos reales del negocio (velocidad, móvil, llamada a la acción, reservas). Úsala cuando digan /copia, «comenta COPIA», «cópiame esta web», «replica esta web», «clona esta página», «hazme la web de mi cliente mejorada» o peguen la URL de una web para copiarla.
---

# /copia: te copio cualquier web

Al terminar, el usuario tiene en `~/Webs/<nombre>/` la copia de la web (`copia/index.html`), su comparación con el
original y, si la pide, la versión mejorada (`mejorada/index.html`) lista para enseñar en la llamada. El método y el
prompt exacto están en `DOCUMENTO.md`: léelo entero antes de empezar.

Español de España, cercano y corto. **Una pregunta cada vez.**

## Reglas
- **Para qué sirve:** copiar la web de TU cliente (o una que tú tengas derecho a usar) para enseñarle cómo quedaría
  mejorada, o aprender la estructura de una referencia. Si la web es de una marca ajena, la copia es solo de práctica
  en local: no se publica con sus logos, fotos ni textos. Díselo una vez, sin sermones.
- **Nunca publiques sin el OK** del usuario (Vercel, Cloudflare, dominios, repos).
- **Nunca inventes** datos del negocio en la versión mejorada (precios, reseñas, horarios, cifras): lo que falte va como
  `[[pendiente: qué falta]]` visible, y al final das la lista.
- Las imágenes del original se usan como referencia; en la copia de práctica pon marcadores del mismo tamaño si no son
  del cliente.

## El recorrido
### Paso 0. Herramientas
`python3 -c "import playwright, PIL"`. Si falla: `pip install playwright pillow && python3 -m playwright install chromium`.

### Paso 1. La web (1 pregunta)
¿Qué web copiamos y es de tu cliente o es una referencia? Nombre de la carpeta en minúsculas con guiones.

### Paso 2. Captura
`python3 scripts/captura.py <url> --salida ~/Webs/<nombre>/original`. Mira `escritorio.png` y `movil.png` (léelas
como imagen) y `estilo.json` / `textos.md`.

### Paso 3. Replicar
Sigue el **prompt exacto** de `DOCUMENTO.md` con la captura, la ficha de estilo y los textos. Un solo archivo
`~/Webs/<nombre>/copia/index.html` con CSS dentro, móvil incluido.

### Paso 4. Comparar y arreglar (bucle)
`python3 scripts/comparar.py ~/Webs/<nombre>/original/escritorio.png ~/Webs/<nombre>/copia/index.html`.
Mira `comparacion.png`, arregla las franjas que más difieren y repite hasta que la similitud deje de subir (suele
quedar por encima del 85 % en 2 o 3 vueltas). Ábrela en el navegador: `open ~/Webs/<nombre>/copia/index.html`.

### Paso 5. Mejorarla para la llamada (si es de un cliente)
Copia a `mejorada/` y aplica las mejoras de `DOCUMENTO.md` con sus datos reales. Enséñale el antes y el después
lado a lado y la lista de pendientes. Publicar, solo con su OK.
