# Carousel patterns — estructuras probadas

Para carruseles de IG de 5-10 slides. El primer slide es la cover, el último el CTA. Lo de en medio es el contenido.

## Estructuras

### 1. Hook → Problem → Solution → Proof → CTA (5-7 slides)

| Slide | Función | Ejemplo |
|---|---|---|
| 1 | **Hook** | "Por esto tu marca no vende" |
| 2 | **Problema 1** | "Tu copy habla de ti, no del cliente" |
| 3 | **Problema 2** | "No tienes diferenciador real" |
| 4 | **Solución** | "Empieza por X, no por Y" |
| 5 | **Proof / case study** | "Cómo aplicamos esto y subimos 40%" |
| 6 | **CTA** | "Guarda este post / cuéntame en comentarios" |

### 2. Listicle (5-10 slides)

| Slide | Función |
|---|---|
| 1 | Cover: "7 cosas que…" |
| 2-8 | Una cosa por slide, headline grande + bullet |
| 9 | "¿Cuál te llevas?" |
| 10 | CTA + handle |

### 3. Antes / después (5 slides)

| Slide | Función |
|---|---|
| 1 | Cover con "Antes" prominente |
| 2 | El "antes" detallado |
| 3 | "Hicimos esto" (cambio aplicado) |
| 4 | El "después" detallado |
| 5 | CTA |

### 4. Historia / case study (7-10 slides)

| Slide | Función |
|---|---|
| 1 | Hook tipo "Te voy a contar cómo…" |
| 2-3 | Contexto inicial |
| 4-6 | Acción / proceso |
| 7-8 | Resultado / takeaway |
| 9-10 | Lección + CTA |

## Reglas de diseño

1. **Cover es lo más importante**: 80% del éxito está ahí. Headline gigante.
2. **Cada slide debe poder leerse en 1 segundo**: cero párrafos largos.
3. **Consistencia visual**: mismo color de fondo, misma tipografía, mismo formato a través de todos los slides.
4. **Numera los slides** (1/7, 2/7…) para que la gente sepa cuántos quedan.
5. **Última slide siempre tiene CTA**: comentar, guardar, dar follow, ir al link.

## Prompts para Higgsfield (gpt-image-2)

Cada slide es un prompt separado. El prompt debe incluir:

- Texto del slide entre comillas dobles (debe aparecer renderizado en la imagen)
- Background color HEX exacto
- Primary text color HEX exacto
- Fuente del headline + tamaño
- Aspect ratio 1:1
- Position (centrado, top, bottom)

Ejemplo:

```
Square 1:1 instagram slide. Background color exactly #1A1A1A. 
Large headline rendered in Inter Bold 64px, color exactly #FF5733, centered: "POR ESTO TU MARCA NO VENDE". 
Below in Inter Regular 24px, color #FFFFFF, centered: "Slide 1 de 7". 
Small "@handle" in bottom-right corner, Inter Regular 14px, color #888888. 
Minimal, editorial, agency quality. No decorative elements. Text must be perfectly legible.
```
