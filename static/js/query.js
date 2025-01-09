import { updateChatBox } from './chatBox.js';

export async function sendQuery(queryInput, sessionId, roomId, friendlyName) {
    if (!queryInput) return;

    const chatBox = document.getElementById('chat-box');

    const userMessage = document.createElement('div');
    userMessage.className = 'message user-message self';
    userMessage.innerHTML = `<span class="user">You:</span> ${queryInput}`;
    chatBox.appendChild(userMessage);

    const aiMessage = document.createElement('div');
    aiMessage.className = 'message ai-message';
    aiMessage.innerHTML = `<span class="ai">AI:</span> `;
    chatBox.appendChild(aiMessage);

    try {
        const response = await fetch('/chat/query/stream', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: queryInput, session_id: sessionId, room_id: roomId, friendly_name: friendlyName }),
        });

        if (!response.ok) {
            aiMessage.innerHTML += `<span style="color: red;">Error: Unable to fetch response</span>`;
            return;
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let done = false;

        while (!done) {
            const { value, done: readerDone } = await reader.read();
            done = readerDone;

            if (value) {
                const chunk = decoder.decode(value, { stream: true });
                try {
                    const json = JSON.parse(chunk);
                    if (json.response) {
                        aiMessage.innerHTML += json.response;
                    }
                } catch (e) {
                    console.error("Error parsing chunk:", chunk, e);
                }
            }
        }
    } catch (error) {
        aiMessage.innerHTML += `<span style="color: red;">Error: ${error.message}</span>`;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
    document.getElementById('user-input').value = '';
}
