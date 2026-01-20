// RIPPLE EFFECT en botones
function createRipple(event) {
  const button = event.currentTarget;
  const rect = button.getBoundingClientRect();
  const size = Math.max(rect.width, rect.height);
  const x = event.clientX - rect.left - size / 2;
  const y = event.clientY - rect.top - size / 2;

  const ripple = document.createElement("span");
  ripple.className = "ripple";
  ripple.style.width = ripple.style.height = size + "px";
  ripple.style.left = x + "px";
  ripple.style.top = y + "px";

  button.appendChild(ripple);
  setTimeout(() => ripple.remove(), 600);
}

document.querySelectorAll("button").forEach(btn => {
  btn.addEventListener("click", createRipple);
});

// TEMA TOGGLE
const themeBtn = document.getElementById("theme-btn");
const htmlElement = document.documentElement;

// Cargar tema guardado
const savedTheme = localStorage.getItem("theme") || "dark";
if (savedTheme === "light") {
  document.body.classList.add("light-mode");
  themeBtn.textContent = "🌚";
}

themeBtn.addEventListener("click", () => {
  document.body.classList.toggle("light-mode");
  const isLight = document.body.classList.contains("light-mode");
  localStorage.setItem("theme", isLight ? "light" : "dark");
  themeBtn.textContent = isLight ? "🌚" : "🌙";
});

// CHAT LOGIC
const chatLog = document.getElementById("chat-log");
const statusBar = document.getElementById("status");
const form = document.getElementById("chat-form");
const input = document.getElementById("message");
const sendButton = document.getElementById("send-btn");

let conversationHistory = [];
let loading = false;

// Crear typing indicator
function createTypingIndicator() {
  const bubble = document.createElement("div");
  bubble.className = "message assistant typing-indicator";
  bubble.id = "typing-indicator";
  
  const label = document.createElement("div");
  label.className = "sender";
  label.textContent = "Asistente";
  
  const content = document.createElement("div");
  content.className = "text";
  content.innerHTML = '<span></span><span></span><span></span>';
  
  bubble.appendChild(label);
  bubble.appendChild(content);
  chatLog.appendChild(bubble);
  chatLog.scrollTop = chatLog.scrollHeight;
  return bubble;
}

function removeTypingIndicator() {
  const indicator = document.getElementById("typing-indicator");
  if (indicator) {
    indicator.remove();
  }
}

function appendMessage(sender, text) {
  const bubble = document.createElement("div");
  bubble.className = `message ${sender === "Usuario" ? "user" : sender === "Asistente" ? "assistant" : "system"}`;

  const label = document.createElement("div");
  label.className = "sender";
  label.textContent = sender;

  const content = document.createElement("div");
  content.className = "text";
  content.textContent = text;

  bubble.appendChild(label);
  bubble.appendChild(content);
  chatLog.appendChild(bubble);
  chatLog.scrollTop = chatLog.scrollHeight;
}

function setLoading(state) {
  loading = state;
  const emoji = state ? "⏳" : "🟢";
  const text = state ? "Pensando..." : "Listo para ayudarte";
  statusBar.textContent = `${emoji} ${text}`;
  input.disabled = state;
  sendButton.disabled = state;
  sendButton.style.opacity = state ? "0.6" : "1";
}

function showInitialMessage() {
  if (window.initialAssistantMessage) {
    appendMessage("Asistente", window.initialAssistantMessage);
    conversationHistory.push({ sender: "Asistente", text: window.initialAssistantMessage });
  }
}

async function sendMessage(event) {
  event.preventDefault();
  if (loading) return;

  const text = input.value.trim();
  if (!text) return;

  // Agregar mensaje del usuario
  appendMessage("Usuario", text);
  input.value = "";
  input.focus();

  setLoading(true);
  createTypingIndicator();

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: text,
        history: conversationHistory,
      }),
    });

    const data = await response.json();
    removeTypingIndicator();

    if (!data.success) {
      appendMessage("Sistema", data.error || "No pude procesar tu solicitud.");
      return;
    }

    appendMessage("Asistente", data.response);
    conversationHistory = data.history || conversationHistory;
  } catch (error) {
    removeTypingIndicator();
    appendMessage("Sistema", "❌ Error de red. Intenta de nuevo.");
    console.error(error);
  } finally {
    setLoading(false);
    input.focus();
  }
}

form.addEventListener("submit", sendMessage);
showInitialMessage();
