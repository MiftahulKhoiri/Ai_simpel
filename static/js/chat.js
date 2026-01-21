let lastQuestion = "";
let typingEl = null;

function addMessage(text, sender) {
    const chatBox = document.getElementById("chat-box");
    const msg = document.createElement("div");
    msg.className = "message " + sender;
    msg.innerText = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msg;
}

function showTyping() {
    typingEl = addMessage("AI sedang mengetik...", "ai");
    typingEl.classList.add("typing");
}

function hideTyping() {
    if (typingEl) {
        typingEl.remove();
        typingEl = null;
    }
}

function sendMessage() {
    const input = document.getElementById("user-input");
    const text = input.value.trim();
    if (!text) return;

    lastQuestion = text;
    addMessage(text, "user");
    input.value = "";

    showTyping();

    fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: text })
    })
    .then(res => res.json())
    .then(data => {
        hideTyping();

        const aiMsg = addMessage(data.answer, "ai");

        if (!data.known) {
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

    // AUTO RESIZE HEIGHT
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

    // fokus otomatis
    textarea.focus();
}