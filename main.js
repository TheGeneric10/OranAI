const chatForm = document.getElementById("chat-form");
const promptInput = document.getElementById("prompt");
const historyPanel = document.getElementById("history");
const modelSelect = document.getElementById("model");
const clearButton = document.getElementById("clear-history");

const STORAGE_KEY = "oranai-history";

const knowledgeSnippets = {
  greeting: [
    "Hi! I'm OranAI. Ready to help.",
    "Hello! OranAI online.",
    "Hey there — OranAI here."
  ],
  skills: [
    "I can outline plans, summarize ideas, and walk through logic step-by-step.",
    "I can brainstorm, explain concepts, and keep context of the chat history.",
    "I can help with ideas, quick answers, and structured responses."
  ],
  planning: [
    "Clarify the goal, list steps, execute in order, then review.",
    "Start with the outcome, gather inputs, run the steps, and validate.",
    "Define scope, break into tasks, do the work, and verify."
  ],
  explanation: [
    "Let's break it down into the key pieces and explain each one clearly.",
    "Here's the concept with a straightforward explanation.",
    "I'll summarize the idea and then add a quick example."
  ],
  fallback: [
    "Here is a quick take: ",
    "Here is a simple answer: ",
    "Here is a thoughtful response: "
  ]
};

const state = {
  history: loadHistory(),
  model: modelSelect.value
};

function loadHistory() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch (error) {
    return [];
  }
}

function saveHistory() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.history));
}

function formatTime(date) {
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function addMessage({ role, content, model }) {
  const message = {
    id: crypto.randomUUID(),
    role,
    model,
    content,
    timestamp: new Date().toISOString()
  };
  state.history.push(message);
  saveHistory();
  renderHistory();
}

function renderHistory() {
  historyPanel.innerHTML = "";
  state.history.forEach((message) => {
    const wrapper = document.createElement("div");
    wrapper.className = `message ${message.role === "ai" ? "message--ai" : ""}`;

    const meta = document.createElement("div");
    meta.className = "message__meta";
    const time = formatTime(new Date(message.timestamp));
    const label = message.role === "ai" ? `OranAI (${message.model})` : "You";
    meta.textContent = `${label} · ${time}`;

    const content = document.createElement("div");
    content.className = "message__content";
    content.textContent = message.content;

    wrapper.append(meta, content);
    historyPanel.append(wrapper);
  });

  historyPanel.scrollTop = historyPanel.scrollHeight;
}

function pickRandom(items) {
  return items[Math.floor(Math.random() * items.length)];
}

function buildResponse(prompt, model) {
  const lowerPrompt = prompt.toLowerCase();
  const responseLines = [];
  const intents = {
    greeting: /(hello|hi|hey|yo)\b/,
    skills: /(what can you do|help|capabilities|features)/,
    plan: /(plan|steps|roadmap|strategy)/,
    explain: /(explain|why|how does|what is)/,
    summarize: /(summary|summarize|recap|tl;dr)/
  };

  if (intents.greeting.test(lowerPrompt)) {
    responseLines.push(pickRandom(knowledgeSnippets.greeting));
  }

  if (intents.skills.test(lowerPrompt)) {
    responseLines.push(pickRandom(knowledgeSnippets.skills));
  }

  if (intents.plan.test(lowerPrompt)) {
    responseLines.push(`Plan: ${pickRandom(knowledgeSnippets.planning)}`);
  }

  if (intents.explain.test(lowerPrompt)) {
    responseLines.push(pickRandom(knowledgeSnippets.explanation));
  }

  if (intents.summarize.test(lowerPrompt) && state.history.length > 0) {
    const recent = state.history.slice(-3).map((item) => item.content).join(" | ");
    responseLines.push(`Summary of recent context: ${recent}`);
  }

  if (!responseLines.length) {
    const summary = `${pickRandom(knowledgeSnippets.fallback)}${prompt.trim()}`;
    responseLines.push(summary);
  }

  if (model === "oran-t1") {
    responseLines.push(
      "Mode: Oran-t1 focuses on thorough, high-clarity answers with balanced speed."
    );
    responseLines.push("Tip: Ask for structured plans or step-by-step reasoning.");
  } else {
    responseLines.push("Mode: Oran-0.7 is optimized for quick replies.");
  }

  if (state.history.length > 0) {
    const recent = state.history.slice(-3).map((item) => item.content).join(" | ");
    responseLines.push(`Context echo: ${recent}`);
  }

  return responseLines.join("\n");
}

chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const prompt = promptInput.value.trim();
  if (!prompt) return;

  addMessage({ role: "user", content: prompt, model: "" });
  const response = buildResponse(prompt, state.model);
  addMessage({ role: "ai", content: response, model: state.model });

  promptInput.value = "";
});

modelSelect.addEventListener("change", (event) => {
  state.model = event.target.value;
});

clearButton.addEventListener("click", () => {
  state.history = [];
  saveHistory();
  renderHistory();
});

renderHistory();
