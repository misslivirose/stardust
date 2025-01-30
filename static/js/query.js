import { updateChatBox } from "./chatBox.js";
import { updateSuggestions } from "./get_suggestions.js";
import { updatePDFViewer } from "./getPDF.js";

export async function sendQuery(queryInput, sessionId, roomId, friendlyName) {
  if (!queryInput) return;

  const chatBox = document.getElementById("chat-box");

  const userMessage = document.createElement("div");
  userMessage.className = "message user-message self";
  userMessage.innerHTML = `<span class="user">You:</span> ${queryInput}`;
  chatBox.appendChild(userMessage);

  const aiMessage = document.createElement("div");
  aiMessage.className = "message ai-message";
  aiMessage.innerHTML = `<span class="ai">AI:</span> `;
  chatBox.appendChild(aiMessage);

  let rawResponse = ""; // Capture raw streamed response

  try {
    const response = await fetch("/chat/query/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: queryInput,
        session_id: sessionId,
        room_id: roomId,
        friendly_name: friendlyName,
      }),
    });

    if (!response.ok) {
      aiMessage.innerHTML += `<span style="color: red;">Error: Unable to fetch response</span>`;
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let done = false;

    while (!done) {
      const { value, done: readerDone } = await reader.read();
      done = readerDone;

      if (value) {
        const chunk = decoder.decode(value, { stream: true });
        rawResponse += chunk; // Accumulate the raw streamed response

        // Try updating the HTML live
        aiMessage.innerHTML += chunk;
      }
    }

    console.log("Raw AI Response:", rawResponse); // Debugging log

    // Ensure finalResponse is not empty before calling updateSuggestions
    if (rawResponse.trim().length > 0) {
      updateSuggestions(rawResponse);
      updatePDFViewer(rawResponse);
    } else {
      console.warn(
        "Skipping updateSuggestions and PDFViewer: rawResponse is empty",
      );
    }
  } catch (error) {
    aiMessage.innerHTML += `<span style="color: red;">Error: ${error.message}</span>`;
  }

  chatBox.scrollTop = chatBox.scrollHeight;
  document.getElementById("user-input").value = "";
}
