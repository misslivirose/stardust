export function getRoomId() {
    let roomId = localStorage.getItem('room_id') || prompt('Enter a chat room ID:');
    if (!roomId) {
        roomId = 'default-room';
    }
    localStorage.setItem('room_id', roomId);
    return roomId;
}

export function getSessionId() {
    let sessionId = localStorage.getItem('session_id') || generateSessionId();
    localStorage.setItem('session_id', sessionId);
    return sessionId;
}

export function setSessionId(newId) {
    localStorage.setItem('session_id', newId)
}

function generateSessionId() {
    return 'session-' + Math.random().toString(36).substr(2, 9);
}
