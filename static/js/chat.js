let lastQuestion = "";
let typingEl = null;

const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");

/* ===============================
   UTIL
================================ */

function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = "message " + sender;
    msg.innerText = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msg;
}

/* ===============================
   TYPING INDICATOR
================================ */

function showTyping() {
    hideTyping(); // pastikan tidak dobel
    typingEl = addMessage("AI sedang mengetik...", "ai");
    typingEl.classList.add("typing");
}

function hideTyping() {
    if (typingEl) {
        typingEl.remove();
        typingEl = null;
    }
}

/* ===============================
   INPUT HANDLING (MOBILE FRIENDLY)
================================ */

// auto-grow textarea utama
input.addEventListener("input", () => {
    input.style.height = "auto";
    input.style.height = input.scrollHeight + "px";
});

// Enter = kirim, Shift+Enter = baris baru
input.addEventListener("keydown", e => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

/* ===============================
   SEND MESSAGE
================================ */

function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    lastQuestion = text;
    addMessage(text, "user");

    input.value = "";
    input.style.height = "auto";

    showTyping();

    fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: text })
    })
    .then(res => res.json())
    .then(data => {
        hideTyping();

        const answerText = data.answer || "Maaf, saya belum tahu jawabannya.";
        const aiMsg = addMessage(answerText, "ai");

        if (data.known === false) {
            const learnBox = document.createElement("div");
            learnBox.className = "learn-box";

            const btn = document.createElement("button");
            btn.innerText = "Ajari AI";
            btn.onclick = () => teachAI(learnBox);

            learnBox.appendChild(btn);
            aiMsg.appendChild(learnBox);
        }
    })
    .catch(() => {
        hideTyping();
        addMessage("Terjadi kesalahan server.", "ai");
    });
}

/* ===============================
   TEACH AI
================================ */

function teachAI(container) {
    container.innerHTML = "";

    const textarea = document.createElement("textarea");
    textarea.placeholder = "Masukkan jawaban...";
    textarea.rows = 1;
    textarea.style.width = "100%";
    textarea.style.resize = "none";
    textarea.style.padding = "8px";
    textarea.style.fontSize = "14px";
    textarea.style.borderRadius = "8px";
    textarea.style.border = "1px solid #ccc";
    textarea.style.marginTop = "6px";

    // auto-grow textarea belajar
    textarea.addEventListener("input", () => {
        textarea.style.height = "auto";
        textarea.style.height = textarea.scrollHeight + "px";
    });

    const btn = document.createElement("button");
    btn.innerText = "Simpan";
    btn.style.marginTop = "6px";
    btn.style.background = "#ff9800";
    btn.style.border = "none";
    btn.style.color = "white";
    btn.style.padding = "6px 12px";
    btn.style.borderRadius = "8px";
    btn.style.cursor = "pointer";

    btn.onclick = () => {
        const answer = textarea.value.trim();
        if (!answer) return;

        fetch("/learn", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                question: lastQuestion.toLowerCase(),
                answer: answer
            })
        })
        .then(res => res.json())
        .then(() => {
            addMessage("Terima kasih, saya sudah belajar 👍", "ai");
            container.remove();
        });
    };

    container.appendChild(textarea);
    container.appendChild(btn);
    textarea.focus();
}