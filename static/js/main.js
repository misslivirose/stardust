import { connectWebSocket } from './websocket.js';
import { updateChatBox } from './chatBox.js';
import { getRoomId, getSessionId } from './session.js';
import { sendQuery } from './query.js';

const roomId = getRoomId();
const sessionId = getSessionId();
const friendlyName = document.getElementById('friendly-name').value;

connectWebSocket(roomId, (data) => {
    if (data.history) {
        updateChatBox(data.history);
    }
});

window.sendQuery = () => {
    const queryInput = document.getElementById('user-input').value;
    sendQuery(queryInput, sessionId, roomId, friendlyName);
};
