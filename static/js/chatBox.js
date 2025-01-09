import { getSessionId } from './session.js';

export function updateChatBox(history) {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = ''; // Clear existing messages

    history.forEach(message => {
        const userMessage = document.createElement('div');
        userMessage.className = `message user-message ${message.user === getSessionId() ? 'self' : 'other'}`;
        userMessage.innerHTML = `<span class="user">${message.user}:</span> ${message.message}`;
        chatBox.appendChild(userMessage);

        if (message.ai) {
            const aiMessage = document.createElement('div');
            aiMessage.className = 'message ai-message';
            aiMessage.innerHTML = `<span class="ai">AI:</span> ${message.ai}`;
            chatBox.appendChild(aiMessage);
        }
    });

    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}
