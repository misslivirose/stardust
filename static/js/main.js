import { connectWebSocket } from "./websocket.js";
import { updateChatBox } from "./chatBox.js";
import { getRoomId, getSessionId, setSessionId } from "./session.js";
import { sendQuery } from "./query.js";

export const roomId = getRoomId();
export let sessionId = getSessionId();
export let friendlyName = ""; // TODO REMOVE

document.getElementById("friendly-name").placeholder = sessionId;

connectWebSocket(roomId, (data) => {
  if (data.history) {
    updateChatBox(data.history);
  }
});

window.sendQuery = () => {
  const queryInput = document.getElementById("user-input").value;
  sendQuery(queryInput, sessionId, roomId, friendlyName);
};

window.setNewId = () => {
  const newId = document.getElementById("friendly-name").value;
  console.log("New sessionId set: " + newId);
  setSessionId(newId);
  sessionId = newId;
};

window.getSessionId = () => {
  return sessionId;
};

document
  .getElementById("user-input")
  .addEventListener("keypress", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault(); // Prevent line break
      sendQuery();
    }
  });
