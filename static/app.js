const form = document.getElementById("spoon-form");
const steps = document.getElementById("steps");
const details = document.getElementById("details");
const errorBox = document.getElementById("error");

const createStep = (label, content, highlight = false) => {
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

const formatPhonemes = (collection) =>
  collection.map((line) => line.join(" ")).join("  |  ");

const renderDetails = (data) => {
  details.innerHTML = "";
  const tiles = [
    {
      title: "Original",
      body: data.original_words.join(" → "),
    },
    {
      title: "Phonemes",
      body: formatPhonemes(data.phonemes),
    },
    {
      title: "Swapped",
      body: data.swapped_phonemes.map((p) => p.join(" ")).join("  |  "),
    },
  ];

  if (data.sample_result.length) {
    tiles.push({
      title: "Result",
      body: data.sample_result.join(" → "),
    });
  }

  tiles.forEach((tile) => {
    const card = document.createElement("div");
    card.className = "tile";
    const title = document.createElement("h3");
    title.textContent = tile.title;
    const body = document.createElement("p");
    body.textContent = tile.body;
    card.appendChild(title);
    card.appendChild(body);
    details.appendChild(card);
  });
};

const renderSteps = (data) => {
  steps.innerHTML = "";
  const [first, second] = data.original_words;
  const sequence = [
    {
      label: "Words",
      content: `${first} + ${second}`,
    },
    {
      label: "Phonemes",
      content: data.phonemes.map((p) => p.join(" ")).join("  |  "),
    },
    {
      label: "Sound swap",
      content: data.swapped_phonemes.map((p) => p.join(" ")).join("  |  "),
      highlight: true,
    },
    {
      label: "Spoonerism",
      content:
        data.sample_result.length > 0
          ? data.sample_result.join(" + ")
          : "No matches found yet.",
    },
  ];

  sequence.forEach((item, idx) => {
    setTimeout(() => {
      createStep(item.label, item.content, item.highlight);
    }, idx * 520);
  });
};

const showError = (message) => {
  errorBox.textContent = message;
};

const handleSubmit = async (event) => {
  event.preventDefault();
  const phrase = new FormData(form).get("phrase");
  steps.innerHTML = "";
  details.innerHTML = "";
  showError("");

  try {
    const response = await fetch("/api/spoon", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ phrase }),
    });

    const payload = await response.json();
    if (!response.ok) {
      showError(payload.error || "Unable to build a spoonerism.");
      return;
    }

    renderSteps(payload);
    renderDetails(payload);
  } catch (err) {
    showError("Something went wrong. Try again.");
  }
};

form.addEventListener("submit", handleSubmit);
