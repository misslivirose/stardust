let socket;

export function connectWebSocket(roomId, onMessageCallback) {
    socket = new WebSocket(`ws://${window.location.host}/ws/${roomId}`);

    socket.onopen = function () {
        console.log("WebSocket connection established.");
    };

    socket.onerror = function (error) {
        console.error("WebSocket error:", error);
    };

    socket.onmessage = function (event) {
        try {
            // console.log("WebSocket message received:", event.data);
            const data = JSON.parse(event.data);
            onMessageCallback(data);
        } catch (e) {
            console.error("Error parsing WebSocket message:", event.data, e);
        }
    };
}

export function sendWebSocketMessage(message) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify(message));
    } else {
        console.error("WebSocket is not open.");
    }
}
