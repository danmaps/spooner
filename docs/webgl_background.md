## Animated WebGL Background Guide

This note explains how the Spooner web app renders its subtle, animated background using vanilla WebGL. You can use the snippets below to recreate or customize the effect in your own project.

---

### 1. Create a Fullscreen Canvas

Add a canvas just inside `<body>` so it sits behind your UI:

```html
<body class="home">
  <canvas id="home-splash"></canvas>
  <!-- rest of the app -->
</body>
```

Give it fixed positioning and pointer transparency so it doesn’t eat clicks:

```css
#home-splash {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
  z-index: -1;
  opacity: 0.55;
  filter: saturate(145%);
  background: radial-gradient(circle at top right, rgba(40, 180, 255, 0.15), rgba(0,0,0,0.85));
}

@media (prefers-reduced-motion: reduce) {
  #home-splash {
    opacity: 0.2;
  }
}
```

This gradient acts as a graceful fallback if WebGL initialization fails.

---

### 2. Initialize WebGL

We grab the canvas, respect `prefers-reduced-motion`, and bootstrap a WebGL context:

```js
const canvas = document.getElementById("home-splash");
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

if (!prefersReducedMotion.matches && canvas) {
  const gl = canvas.getContext("webgl", { alpha: true, antialias: true });
  if (!gl) {
    canvas.style.opacity = "0.3"; // fallback
  } else {
    startSplash(gl);
  }
} else {
  canvas.style.opacity = "0.2";
}
```

Call `startSplash(gl)` with the shader setup shown below.

---

### 3. Vertex + Fragment Shaders

The vertex shader is a standard fullscreen triangle strip:

```glsl
attribute vec2 position;
varying vec2 vUv;
void main() {
  vUv = position * 0.5 + 0.5;
  gl_Position = vec4(position, 0.0, 1.0);
}
```

The fragment shader uses noise-based fBm layers to paint smooth color blobs:

```glsl
precision mediump float;
uniform vec2 u_resolution;
uniform float u_time;
uniform vec2 u_mouse;
uniform float u_intensity;

float hash(vec2 p) {
  return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float noise(vec2 p) {
  vec2 i = floor(p);
  vec2 f = fract(p);
  float a = hash(i);
  float b = hash(i + vec2(1.0, 0.0));
  float c = hash(i + vec2(0.0, 1.0));
  float d = hash(i + vec2(1.0, 1.0));
  vec2 u = f * f * (3.0 - 2.0 * f);
  return mix(a, b, u.x) + (c - a) * u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
}

float fbm(vec2 p) {
  float value = 0.0;
  float amplitude = 0.5;
  float frequency = 1.0;
  for (int i = 0; i < 4; i++) {
    value += amplitude * noise(p * frequency);
    frequency *= 1.8;
    amplitude *= 0.5;
  }
  return value;
}

void main() {
  vec2 uv = gl_FragCoord.xy / u_resolution.xy;
  vec2 centered = uv - 0.5;
  centered.x *= u_resolution.x / u_resolution.y;
  float time = u_time * 0.15;

  float layer1 = fbm(centered * 1.2 + vec2(time, -time * 0.6));
  float layer2 = fbm(centered * 0.8 - vec2(time * 0.4, -time * 0.3));
  float layer3 = fbm(centered * 2.2 + vec2(-time * 0.8, time * 0.5));
  float combined = layer1 * 0.5 + layer2 * 0.3 + layer3 * 0.2;
  combined += (u_mouse.x - 0.5) * 0.15 + (u_mouse.y - 0.5) * 0.15;

  vec3 colorA = vec3(0.08, 0.19, 0.38);
  vec3 colorB = vec3(0.02, 0.08, 0.12);
  vec3 accent = vec3(0.25, 0.65, 0.58);
  vec3 color = mix(colorB, colorA, combined);
  color += accent * smoothstep(0.4, 0.8, combined);

  float vignette = smoothstep(1.3, 0.2, length(centered));
  vec3 finalColor = color * (0.6 + 0.4 * combined) * vignette * u_intensity;
  float alpha = vignette * 0.6;

  gl_FragColor = vec4(finalColor, alpha);
}
```

The key ingredients:
- **fBm layers** create natural blobby gradients.
- **Mouse input** nudges the colors for subtle interactivity.
- **Vignette** keeps the edges dark so the UI remains legible.

---

### 4. JavaScript Glue

Below is a condensed version of the runtime setup used in `static/app.js`:

```js
const rgb = (r, g, b) => [r / 255, g / 255, b / 255];

function startSplash(gl) {
  const vertexShader = compileShader(gl.VERTEX_SHADER, vertexShaderSource);
  const fragmentShader = compileShader(
    gl.FRAGMENT_SHADER,
    fragmentShaderSource
      .replace("vec3 baseA = vec3(0.08, 0.19, 0.38);", `vec3 baseA = vec3(${rgb(20, 60, 120).join(", ")});`)
  );
  const program = createProgram(vertexShader, fragmentShader);

  const positionLocation = gl.getAttribLocation(program, "position");
  const resolutionLocation = gl.getUniformLocation(program, "u_resolution");
  const timeLocation = gl.getUniformLocation(program, "u_time");
  const mouseLocation = gl.getUniformLocation(program, "u_mouse");
  const intensityLocation = gl.getUniformLocation(program, "u_intensity");

  // Create fullscreen triangle buffer
  const positionBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.bufferData(
    gl.ARRAY_BUFFER,
    new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]),
    gl.STATIC_DRAW
  );

  const mouse = { x: 0.5, y: 0.5 };
  window.addEventListener("pointermove", (event) => {
    mouse.x = event.clientX / window.innerWidth;
    mouse.y = 1 - event.clientY / window.innerHeight;
  }, { passive: true });

  function resizeCanvas() {
    const dpr = window.devicePixelRatio || 1;
    const width = Math.floor(window.innerWidth * dpr);
    const height = Math.floor(window.innerHeight * dpr);
    if (gl.canvas.width !== width || gl.canvas.height !== height) {
      gl.canvas.width = width;
      gl.canvas.height = height;
    }
  }
  window.addEventListener("resize", resizeCanvas);
  resizeCanvas();

  let rafId = null;
  let startTime = performance.now();

  function draw(now) {
    resizeCanvas();
    gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);

    gl.useProgram(program);
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.enableVertexAttribArray(positionLocation);
    gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

    gl.uniform2f(resolutionLocation, gl.canvas.width, gl.canvas.height);
    gl.uniform1f(timeLocation, (now - startTime) * 0.001);
    gl.uniform2f(mouseLocation, mouse.x, mouse.y);
    gl.uniform1f(intensityLocation, 0.7);

    gl.drawArrays(gl.TRIANGLES, 0, 6);
    rafId = requestAnimationFrame(draw);
  }

  draw(performance.now());
}
```

Additional niceties implemented in the app:
- Pause animation when the tab is hidden to save battery.
- Reduce opacity if the user prefers reduced motion.
- Lower opacity or stop animation entirely if WebGL initialization fails.

---

### 5. Customization Ideas

| Knob | Effect |
| --- | --- |
| `rgb()` values | Change color palette; use multiple accent colors or HSL-to-RGB conversion. |
| `u_intensity` | Dial overall brightness; map to a UI slider for user control. |
| Number of fBm layers | More layers yield richer texture but cost more GPU time. |
| Mouse influence | Remove for a passive background or amplify for interactive experiences. |
| Time multiplier | Speed up or slow down the animation; you can also pause on reduced-motion devices. |

Because the shader is plain text, you can even expose the color values and intensity as CSS variables or user settings to keep them in sync with light/dark themes.

---

### 6. Troubleshooting

- **Shader compile errors**: log `gl.getShaderInfoLog` outputs; minor syntax errors will break the effect entirely.
- **Performance**: reduce fBm iterations or the frame rate cap if older devices struggle.
- **Mobile Safari quirks**: ensure the canvas uses `position: fixed` and `pointer-events: none` to avoid scroll issues.

With these pieces, you should be able to spin up your own amorphous WebGL splash and tweak it to match any visual system. Happy shader hacking!
