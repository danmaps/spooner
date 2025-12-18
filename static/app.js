const form = document.getElementById("spoon-form");
const steps = document.getElementById("steps");
const resultsSection = document.querySelector(".results");
const errorBox = document.getElementById("error");
const phraseInput = document.getElementById("phrase");
const splashCanvas = document.getElementById("home-splash");
const debugToggle = document.getElementById("debug-toggle");
const debugPanel = document.getElementById("debug-panel");
const debugList = document.getElementById("debug-list");
const prefersReducedMotion = window.matchMedia(
  "(prefers-reduced-motion: reduce)"
);

const samplePhrases = [
  "trail snacks",
  "crushing blow",
  "jelly beans",
  "hello world",
  "run for",
  "loving shepherd",
  "dental reception",
];

const pickRandomPhrase = () =>
  samplePhrases[Math.floor(Math.random() * samplePhrases.length)];

const setInitialPhrase = () => {
  if (phraseInput && !phraseInput.value) {
    phraseInput.value = pickRandomPhrase();
  }
};

setInitialPhrase();

const resetDebugPanel = () => {
  if (debugPanel) {
    debugPanel.hidden = true;
  }
  if (debugList) {
    debugList.innerHTML = "";
  }
};

const createSimpleStep = (label, content, highlight = false) => {
  const wrapper = document.createElement("div");
  wrapper.className = "step animate-in";

  const small = document.createElement("small");
  small.textContent = label;
  const body = document.createElement("div");
  body.className = "content" + (highlight ? " swap" : "");
  body.textContent = content;

  wrapper.appendChild(small);
  wrapper.appendChild(body);
  steps.appendChild(wrapper);
};

const createChunk = (items, chunkClass) => {
  if (!items.length) {
    return null;
  }
  const chunk = document.createElement("span");
  chunk.className = `chunk ${chunkClass}`;
  items.forEach((item) => {
    const token = document.createElement("span");
    token.className = "chunk-token";
    token.textContent = item;
    chunk.appendChild(token);
  });
  return chunk;
};

const buildWord = (
  phones,
  highlightCount,
  chunkClass,
  swappedPhones,
  swappedHighlightCount
) => {
  const container = document.createElement("div");
  container.className = "phoneme-word";
  const prefixCount = highlightCount || 0;
  const prefix = phones.slice(0, prefixCount);

  const chunkWrapper = document.createElement("div");
  chunkWrapper.className = "chunk-wrap";
  const chunk = createChunk(prefix, chunkClass);
  if (chunk) {
    chunkWrapper.appendChild(chunk);
  } else {
    chunkWrapper.classList.add("chunk-empty");
  }
  container.appendChild(chunkWrapper);

  const tail = document.createElement("span");
  tail.className = "phoneme-tail";

  const originalTail = phones.slice(prefixCount).join(" ") || "—";
  const swappedTail =
    (swappedPhones || []).slice(swappedHighlightCount || 0).join(" ") ||
    originalTail;

  const originalLayer = document.createElement("span");
  originalLayer.className = "tail-layer tail-original";
  originalLayer.textContent = originalTail;

  const swappedLayer = document.createElement("span");
  swappedLayer.className = "tail-layer tail-swapped";
  swappedLayer.textContent = swappedTail;

  tail.appendChild(originalLayer);
  tail.appendChild(swappedLayer);

  container.appendChild(tail);

  return { element: container, chunkWrapper };
};

const createPhonemeRail = ({
  label,
  phonemeSets,
  swappedSets,
  highlightCounts,
  swappedHighlightCounts,
  chunkClasses,
  enableSwap,
}) => {
  const wrapper = document.createElement("div");
  wrapper.className = "step phoneme-step animate-in";
  if (enableSwap) {
    wrapper.classList.add("can-swap");
  }

  const labelLink = document.createElement("a");
  labelLink.className = "phoneme-link";
  labelLink.href = "https://en.wikipedia.org/wiki/ARPABET";
  labelLink.target = "_blank";
  labelLink.rel = "noopener noreferrer";
  labelLink.textContent = label;
  wrapper.appendChild(labelLink);

  const rail = document.createElement("div");
  rail.className = "phoneme-rail";

  const wordNodes = phonemeSets.map((phones, idx) =>
    buildWord(
      phones,
      highlightCounts[idx],
      chunkClasses[idx],
      swappedSets[idx],
      swappedHighlightCounts[idx]
    )
  );

  wordNodes.forEach((node, idx) => {
    rail.appendChild(node.element);
    if (idx === 0) {
      const divider = document.createElement("span");
      divider.className = "divider";
      divider.textContent = "|";
      rail.appendChild(divider);
    }
  });

  wrapper.appendChild(rail);
  steps.appendChild(wrapper);

  if (enableSwap) {
    prepareSwapAnimation(rail);
  }
};

const swapRails = new Set();

const measureSwapDistance = (rail) => {
  const chunkWraps = rail.querySelectorAll(".chunk-wrap");
  if (chunkWraps.length !== 2) {
    return;
  }
  const [first, second] = chunkWraps;
  const firstRect = first.getBoundingClientRect();
  const secondRect = second.getBoundingClientRect();
  const firstShift = secondRect.left - firstRect.left;
  const secondShift = firstRect.left - secondRect.left;
  first.style.setProperty("--swap-shift", `${firstShift}px`);
  second.style.setProperty("--swap-shift", `${secondShift}px`);
};

const prepareSwapAnimation = (rail) => {
  swapRails.add(rail);
  requestAnimationFrame(() => measureSwapDistance(rail));
};

window.addEventListener("resize", () => {
  swapRails.forEach((rail) => measureSwapDistance(rail));
});

const formatScore = (value) => Number(value || 0).toFixed(2);

const renderDebugPairs = (pairs, debugEnabled) => {
  if (!debugPanel || !debugList) {
    return;
  }
  debugList.innerHTML = "";
  if (!debugEnabled || !pairs.length) {
    debugPanel.hidden = true;
    return;
  }
  debugPanel.hidden = false;
  pairs.forEach((pair) => {
    const row = document.createElement("div");
    row.className = "debug-row";
    const [firstWord, secondWord] = pair.words || [];
    const [firstScore, secondScore] = pair.scores || [];
    row.textContent = `[${firstWord} ${formatScore(
      firstScore
    )}, ${secondWord} ${formatScore(secondScore)}]`;
    debugList.appendChild(row);
  });
};

const renderSteps = (data) => {
  swapRails.clear();
  steps.innerHTML = "";
  const [first, second] = data.original_words;
  const prefixSets = data.prefixes || [[], []];
  const prefixLengths = prefixSets.map((chunk) => chunk.length);
  const hasSwap = data.swapped_phonemes && data.swapped_phonemes.length === 2;
  const swappedSets = hasSwap ? data.swapped_phonemes : data.phonemes;
  const swappedCounts = hasSwap
    ? [prefixLengths[1], prefixLengths[0]]
    : prefixLengths;
  const swappedChunkClasses = hasSwap
    ? ["chunk-b", "chunk-a"]
    : ["chunk-a", "chunk-b"];

  createPhonemeRail({
    label: "Phonemes",
    phonemeSets: data.phonemes,
    swappedSets,
    highlightCounts: prefixLengths,
    swappedHighlightCounts: swappedCounts,
    chunkClasses: ["chunk-a", "chunk-b"],
    enableSwap: hasSwap,
  });

  createSimpleStep(
    "Spoonerism",
    data.sample_result.length > 0
      ? data.sample_result.join(" ")
      : "That's not a word!",
    true
  );
  renderDebugPairs(data.ranked_pairs || [], Boolean(data.debug));

  if (resultsSection) {
    resultsSection.classList.remove("is-hidden");
  }
};

const showError = (message) => {
  errorBox.textContent = message;
};

const handleSubmit = async (event) => {
  event.preventDefault();
  const phrase = new FormData(form).get("phrase");
  const debugMode = Boolean(debugToggle && debugToggle.checked);
  steps.innerHTML = "";
  showError("");
  resetDebugPanel();

  try {
    const response = await fetch("/api/spoon", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ phrase, debug: debugMode }),
    });

    const payload = await response.json();
    if (!response.ok) {
      showError(payload.error || "Unable to build a spoonerism.");
      resetDebugPanel();
      return;
    }

    renderSteps(payload);
  } catch (err) {
    showError("Something went wrong. Try again.");
    resetDebugPanel();
  }
};

const hideResults = () => {
  if (resultsSection) {
    resultsSection.classList.add("is-hidden");
  }
  resetDebugPanel();
};

form.addEventListener("submit", (event) => {
  hideResults();
  handleSubmit(event);
});

if (resultsSection) {
  resultsSection.classList.add("is-hidden");
}

const initSplash = () => {
  if (!splashCanvas) {
    return;
  }

  if (prefersReducedMotion.matches) {
    splashCanvas.style.opacity = "0.2";
    return;
  }

  const gl = splashCanvas.getContext("webgl", { alpha: true, antialias: true });
  if (!gl) {
    splashCanvas.style.opacity = "0.3";
    return;
  }

  const vertexShaderSource = `
    attribute vec2 position;
    varying vec2 vUv;
    void main() {
      vUv = position * 0.5 + 0.5;
      gl_Position = vec4(position, 0.0, 1.0);
    }
  `;
  const rgb = (r, g, b) => [r / 255, g / 255, b / 255];

  const fragmentShaderSource = `
    precision mediump float;
    uniform vec2 u_resolution;
    uniform float u_time;
    uniform vec2 u_mouse;
    uniform float u_intensity;
    varying vec2 vUv;

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


      vec3 baseA = vec3(${rgb(20, 60, 120).join(", ")});
      vec3 baseB = vec3(${rgb(5, 15, 30).join(", ")});
      vec3 accent = vec3(${rgb(64, 200, 180).join(", ")});
      vec3 color = mix(baseB, baseA, combined);
      color += accent * smoothstep(0.4, 0.8, combined);

      float vignette = smoothstep(1.3, 0.2, length(centered));
      vec3 finalColor = color * (0.6 + 0.4 * combined) * vignette * u_intensity;
      float alpha = vignette * 0.6;

      gl_FragColor = vec4(finalColor, alpha);
    }
  `;

  const compileShader = (type, source) => {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      console.error(gl.getShaderInfoLog(shader));
      gl.deleteShader(shader);
      return null;
    }
    return shader;
  };

  const createProgram = (vertexShader, fragmentShader) => {
    const program = gl.createProgram();
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
      console.error(gl.getProgramInfoLog(program));
      gl.deleteProgram(program);
      return null;
    }
    return program;
  };

  const vertexShader = compileShader(gl.VERTEX_SHADER, vertexShaderSource);
  const fragmentShader = compileShader(gl.FRAGMENT_SHADER, fragmentShaderSource);
  if (!vertexShader || !fragmentShader) {
    splashCanvas.style.opacity = "0.25";
    return;
  }

  const program = createProgram(vertexShader, fragmentShader);
  if (!program) {
    splashCanvas.style.opacity = "0.25";
    return;
  }

  const positionLocation = gl.getAttribLocation(program, "position");
  const resolutionLocation = gl.getUniformLocation(program, "u_resolution");
  const timeLocation = gl.getUniformLocation(program, "u_time");
  const mouseLocation = gl.getUniformLocation(program, "u_mouse");
  const intensityLocation = gl.getUniformLocation(program, "u_intensity");

  const positionBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
  gl.bufferData(
    gl.ARRAY_BUFFER,
    new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]),
    gl.STATIC_DRAW
  );

  const mouse = { x: 0.5, y: 0.5 };
  window.addEventListener(
    "pointermove",
    (event) => {
      mouse.x = event.clientX / window.innerWidth;
      mouse.y = 1 - event.clientY / window.innerHeight;
    },
    { passive: true }
  );

  const resizeCanvas = () => {
    const dpr = window.devicePixelRatio || 1;
    const width = Math.floor(window.innerWidth * dpr);
    const height = Math.floor(window.innerHeight * dpr);
    if (splashCanvas.width !== width || splashCanvas.height !== height) {
      splashCanvas.width = width;
      splashCanvas.height = height;
    }
  };

  window.addEventListener("resize", resizeCanvas, { passive: true });
  resizeCanvas();

  let rafId = null;
  let startTime = performance.now();

  const drawFrame = (now) => {
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

    rafId = requestAnimationFrame(drawFrame);
  };

  const start = () => {
    if (rafId === null) {
      startTime = performance.now();
      rafId = requestAnimationFrame(drawFrame);
    }
  };

  const stop = () => {
    if (rafId !== null) {
      cancelAnimationFrame(rafId);
      rafId = null;
    }
  };

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      stop();
    } else if (!prefersReducedMotion.matches) {
      start();
    }
  });

  const motionListener = (event) => {
    if (event.matches) {
      stop();
      splashCanvas.style.opacity = "0.2";
    } else {
      splashCanvas.style.opacity = "0.55";
      start();
    }
  };

  if (prefersReducedMotion.addEventListener) {
    prefersReducedMotion.addEventListener("change", motionListener);
  } else if (prefersReducedMotion.addListener) {
    prefersReducedMotion.addListener(motionListener);
  }

  start();
};

initSplash();
