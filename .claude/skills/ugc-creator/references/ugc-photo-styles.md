# UGC product photo styles — para ecommerce

Tres estilos cubren el 90% de necesidades. Aquí está cuándo usar cada uno.

## 1. Packshot (foto técnica)

**Uso**: catálogo, marketplace (Amazon, Mercado Libre), tienda principal.

**Características**:
- Fondo blanco puro o gris muy claro
- Producto perfectamente centrado, recortado
- Sin sombras dramáticas (sombra suave OK)
- Sin contexto, sin manos, sin ambiente
- Iluminación uniforme

**Aspect**: 1:1 (Amazon, IG), 1:1.25 (Amazon main), 4:5 (Shopify hero)

**Prompt baseline**:
```
Product photography packshot. <Producto detalle>. Pure white background (#FFFFFF). Centered, isometric or slight angle (15-30 degrees from front). Soft diffused lighting, no harsh shadows. No hands, no people, no extra props. High resolution, sharp focus on every detail. Ecommerce-ready, suitable for marketplace listing.
```

## 2. Lifestyle (producto en uso)

**Uso**: redes sociales, ads, página de producto secundaria, email marketing.

**Características**:
- Producto en uso por una persona (manos al menos visibles)
- Ambiente realista que conecta con el buyer persona
- Iluminación natural cálida
- Composición narrativa (cuenta una historia)
- Modelo demográficamente alineado con audiencia

**Aspect**: 4:5 (IG), 1:1 (cuadrícula), 9:16 (Stories)

**Prompt baseline**:
```
Product lifestyle photography. <Producto> being used by <persona description con etnia/edad/contexto>. Setting: <ambiente — kitchen, office, bathroom, outdoor>. Natural warm daylight, soft shadows. <Producto> is the focal point but feels integrated in the scene. Authentic, not over-styled. Hands and partial body visible. Realistic, mid-shot. No on-screen text.
```

## 3. In-context (producto solo en ambiente)

**Uso**: aesthetic posts, hero sections, branding pieces.

**Características**:
- Producto solo, sin personas
- En ambiente real (escritorio, mesa, repisa)
- Composición de still life
- Iluminación natural
- Puede incluir props complementarios sutiles

**Aspect**: 4:5, 1:1, 16:9 (web hero)

**Prompt baseline**:
```
Still life product photography. <Producto> placed on <surface — wooden desk, marble counter, ceramic plate>. Natural daylight from window left, soft shadows. Minimalist composition with 1-2 subtle complementary props (notebook, plant, ceramic cup). <Producto> is the hero. Warm, editorial, lifestyle magazine aesthetic. No people, no on-screen text.
```

## Reglas universales

1. **Investiga el buyer persona antes de elegir modelo**: edad, etnia, lifestyle. Higgsfield maneja diversidad bien si le das contexto.
2. **Para marketplace**: packshot es obligatorio. Sin esto, no listas.
3. **Para social**: lifestyle > packshot. Engagement es 3-5x mayor.
4. **NO mezcles estilos en un set**: si haces packshot, todos packshot. Si lifestyle, todos lifestyle.
5. **Resolución mínima**: 2048x2048 para marketplace. Higgsfield genera a 2K-4K por default.
6. **NO retoques de modelo**: Higgsfield ya genera personas realistas. Si retocas en post, cuidado con el "uncanny valley" — la imagen pierde feel UGC.
