
// Grab elements from the HTML
const form = document.getElementById("chat-form");
const input = document.getElementById("username");
const chat = document.getElementById("chat");

// Listen for form submission
form.addEventListener("submit", async function (e) {
    e.preventDefault(); // prevent page refresh

    const message = input.value.trim();
    if (!message) return;



// Show user message in chat

    addMessage(message, "user-message");

// Clear input
    input.value = "";

    try {
// Send message to Flask backend
        const response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
body: JSON.stringify({ message: message })
    });
    const data = await response.json();

// Show bot response
    addMessage(data.reply, "bot-message");
} catch (error) {
// If backend is down / error happens
    addMessage("Sorry, I couldn't reach the server.", "bot-message");
}
});

// Function to add a message bubble
function addMessage(text, className) {
   const newMessage = document.createElement("div");
            newMessage.textContent = text;
            newMessage.className = "user-message";

            chatBox.appendChild(newMessage);

            input.value = ""; // clear box

            chatBox.scrollTop = chatBox.scrollHeight; // auto scroll

}