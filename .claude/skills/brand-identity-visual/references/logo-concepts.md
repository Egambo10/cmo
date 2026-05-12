# Logo concepts — referencias

Tipos de logos y cuándo cada uno conviene.

## Tipos

| Tipo | Qué es | Funciona para | Ejemplos reales |
|---|---|---|---|
| **Wordmark** | Solo el nombre, sin símbolo | Marca con nombre corto y único | Google, Coca-Cola, Visa |
| **Lettermark / monograma** | Iniciales | Nombres largos | IBM, HBO, CNN |
| **Símbolo / icono** | Solo gráfico, sin nombre | Marcas ya muy reconocidas | Apple, Nike, Twitter (X) |
| **Lockup (combo)** | Nombre + símbolo juntos | La mayoría de las marcas nuevas | Slack, Spotify, Airbnb |
| **Mascot** | Personaje | F&B, kids, casual | KFC, Pringles, Duolingo |
| **Emblem** | Texto dentro de forma | Tradicional, premium, deportes | Starbucks, Harley-Davidson |
| **Abstract** | Símbolo no representativo | Marcas que quieren ser únicas | Nike swoosh, Pepsi |

## Cómo recomendar

Pregunta al usuario:
- ¿Qué tan corto es el nombre? Corto + fácil → wordmark. Largo → monograma o lockup.
- ¿La marca necesita versatilidad de tamaños chicos (favicon, app icon)? Necesita símbolo solo.
- ¿La cultura es seria o lúdica? Mascots solo en lúdico.
- ¿Aspira a ser global o regional? Global premium → minimalista, evita mascot.

## Reglas de diseño

1. **Escalable**: legible a 16x16 (favicon).
2. **Monocromo funciona**: si solo se ve bien a color, está mal diseñado.
3. **Negativo funciona**: prueba en blanco sobre negro y al revés.
4. **Único**: no se confunde con otro logo conocido (search visual de Google Lens).
5. **Sin texto innecesario**: tagline en logo es para grandes; nuevos no necesitan.
6. **Vector-first**: SVG o vector; nunca raster como master.

## Errores comunes

- 🚫 Logo con efectos 3D o sombras pesadas.
- 🚫 Demasiados colores (>3) en el logo.
- 🚫 Tipografía decorativa difícil de leer.
- 🚫 Símbolo abstracto que "no significa nada" sin razón estratégica.
- 🚫 Copiar un competidor — diferenciación es el punto.

## Prompt baseline para Higgsfield

Cuando uses `higgsfield_logo.sh`, el prompt ya incluye:
- Estilo seleccionado
- Concepto de marca
- Paleta de colores
- Fondo blanco
- Vector-style clean lines
- Sin mockups, sin sombras, sin texturas

Si necesitas ajustar el estilo en iteraciones, pasa un concept brief más específico al script.
