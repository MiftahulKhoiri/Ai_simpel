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

    const input = document.createElement("input");
    input.placeholder = "Masukkan jawaban...";
    input.style.width = "100%";
    input.style.marginTop = "5px";

    const btn = document.createElement("button");
    btn.innerText = "Simpan";
    btn.style.marginTop = "5px";

    btn.onclick = () => {
        const answer = input.value.trim();
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

    container.appendChild(input);
    container.appendChild(btn);
}

document.getElementById("user-input")
    .addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
            e.preventDefault();
            sendMessage();
        }
    });