# Track: negocio existente con documento para ingerir

El usuario tiene un pitch deck, brief, brand book viejo, plan de marketing, o cualquier documento de contexto. El flujo es:

1. **Recibir y leer el documento.**
2. **Extraer lo que ya está respondido.**
3. **Validar con el usuario lo extraído.**
4. **Hacer SOLO las preguntas que faltan.**

Una pregunta por mensaje. Antes de cada pregunta, máximo 2 líneas.

## Paso 1 — Ingesta

Pide al usuario que coloque el documento en `/Users/erikgamboa/Documents/CMO/projects/<slug>/ingest/`. Si lo pegan en chat, guárdalo igual.

Soporta PDF, .docx, .pptx, .md, .txt. Para cada tipo:
- **PDF**: usa el skill `anthropic-skills:pdf` para extraer texto.
- **.docx**: usa `anthropic-skills:docx`.
- **.pptx**: usa `anthropic-skills:pptx`.
- **.md / .txt**: léelo con la herramienta Read.

## Paso 2 — Extracción

Procesa el contenido y busca explícita o implícitamente:

| Pieza | Señales en el documento |
|---|---|
| **Producto/servicio** | "Vendemos…", "Ofrecemos…", "Nuestra solución…" |
| **Problema** | "Los clientes sufren de…", "El mercado tiene un dolor en…" |
| **Audiencia** | Buyer persona, demografía, ICP, perfil de cliente |
| **Diferenciador** | "A diferencia de…", "Lo que nos hace únicos…" |
| **Misión / visión** | Sección explícita, o frases en presentaciones internas |
| **Valores** | Lista usualmente explícita |
| **Tono de voz** | Suele faltar — ojo |
| **Identidad visual actual** | Paleta, logo, fuentes, ejemplos |
| **Competencia** | Mención directa, matrices comparativas |

Crea un resumen interno con lo que **sí encontraste** y lo que **falta**.

## Paso 3 — Validación con el usuario

Antes de inventar nada, valida lo extraído. Por ejemplo:

> *"Leí el documento y entendí lo siguiente. Confírmame si está al día:*
> 
> *• Producto: tienda online de joyería artesanal hecha por mujeres en Oaxaca.*
> *• Cliente ideal: mujer 28-45, ingresos medio-alto, valora historia detrás del producto.*
> *• Diferenciador: cada pieza tiene la historia de la artesana que la hizo.*
> 
> *¿Sigue siendo así o algo cambió desde que escribieron este doc?"*

Si dice "todo correcto" → marca como validado, pasa al Paso 4.
Si dice "esto sí, esto ya no" → captura los cambios.

## Paso 4 — Preguntas para llenar huecos

Mira tu lista de "qué falta" y pregúntalo, **una por mensaje**, usando las preguntas relevantes de `track-new-business.md` o `track-existing-business.md` según el caso.

**Regla crítica**: NO repreguntes lo que ya estaba en el documento y el usuario validó. Eso lo siente como burocracia.

## Paso 5 — Síntesis

Igual que los otros tracks: redacta y valida los 9 bloques (misión, visión, valores, propuesta de valor, posicionamiento, público objetivo, buyer persona, personalidad, tono de voz), uno por mensaje, partiendo de lo extraído + lo completado en Paso 4.

Cuando todo esté validado → escribir `01-plan-estrategico.md`.
