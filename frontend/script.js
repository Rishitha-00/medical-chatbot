async function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, "user");
    input.value = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        addMessage(data.reply, "bot");

    } catch {
        addMessage("Server error. Try again.", "bot");
    }
}

function addMessage(text, sender) {
    const chatBox = document.getElementById("chat-box");
    const msg = document.createElement("div");

    msg.className = sender === "user" ? "user-message" : "bot-message";
    msg.innerHTML = text.replace(/\n/g, "<br>");

    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}