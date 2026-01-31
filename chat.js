// Grab elements from the HTML
const form = document.getElementById("chat-form");
const input = document.getElementById("username");
const chat = document.getElementById("chat");

// Listen for form submission
form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const message = input.value.trim();
    if (!message) return;

    // Show user message
    addMessage(message, "user-message");
    input.value = "";

    try {
        const response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        // Show bot message
        addMessage(data.reply, "bot-message");

    } catch (error) {
        addMessage("Sorry, I couldn't reach the server.", "bot-message");
    }
});

// Add message to chat
function addMessage(text, className) {
    const newMessage = document.createElement("div");
    newMessage.textContent = text;
    newMessage.className = className;

    chat.appendChild(newMessage);
    chat.scrollTop = chat.scrollHeight;
}
