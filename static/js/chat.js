let lastQuestion = "";
let typingEl = null;

const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");

/* ===============================
   SCROLL UTILITY
================================ */

function scrollToBottom(delay = 0) {
    setTimeout(() => {
        chatBox.scrollTop = chatBox.scrollHeight;
    }, delay);
}

/* ===============================
   MESSAGE HANDLER
================================ */

function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = "message " + sender;
    msg.innerText = text;
    chatBox.appendChild(msg);
    scrollToBottom(50);
    return msg;
}

/* ===============================
   TYPING INDICATOR
================================ */

function showTyping() {
    hideTyping(); // cegah dobel
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

// Auto-grow textarea utama
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

// Keyboard muncul → auto scroll
input.addEventListener("focus", () => {
    scrollToBottom(300);
});

// Viewport berubah (keyboard show/hide)
window.addEventListener("resize", () => {
    scrollToBottom(300);
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

        // Jika AI belum tahu → tampilkan tombol ajar
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
   TEACH AI (LEARN MODE)
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

    // Auto-grow textarea belajar
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
        })
        .catch(() => {
            addMessage("Gagal menyimpan jawaban.", "ai");
        });
    };

    container.appendChild(textarea);
    container.appendChild(btn);

    textarea.focus();
    scrollToBottom(300);
}