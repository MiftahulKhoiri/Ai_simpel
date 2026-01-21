function addMessage(text, sender) {
    const chatBox = document.getElementById("chat-box");
    const msg = document.createElement("div");
    msg.className = "message " + sender;
    msg.innerText = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById("user-input");
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: text })
    })
    .then(res => res.json())
    .then(data => {
        if (data.answer) {
            addMessage(data.answer, "ai");
        } else {
            addMessage("Saya belum tahu jawabannya.", "ai");
        }
    })
    .catch(() => {
        addMessage("Terjadi kesalahan server.", "ai");
    });
}

// Kirim dengan Enter
document.getElementById("user-input")
    .addEventListener("keypress", function(e) {
        if (e.key === "Enter") sendMessage();
    });