
document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    const input = document.getElementById("username");
    const chatBox = document.getElementById("chat");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // stop page refresh

        const message = input.value.trim();

        if (message !== "") {
            const newMessage = document.createElement("div");
            newMessage.textContent = message;
            newMessage.className = "user-message";

            chatBox.appendChild(newMessage);

            input.value = ""; // clear box

            chatBox.scrollTop = chatBox.scrollHeight; // auto scroll
        }
    });

});
