import { sendQuery } from "./query.js";
import { roomId, sessionId } from "./main.js";

export async function updateSuggestions(message) {
  console.log(
    "Requesting updated suggestions from latest AI response: " + message,
  );
  try {
    // Send a request to your API endpoint
    const response = await fetch("/recommendation", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: message,
      }),
    });

    // Parse the JSON response
    const data = await response.json();
    console.log(data);
    // Extract the suggestions (adjust based on your API response structure)
    const suggestions = data.questions;

    // Get all button elements inside the suggestions box
    const buttons = document.querySelectorAll(".suggestions-box button");

    // Update the text of each button with the new suggestions
    suggestions.forEach((suggestion, index) => {
      if (buttons[index]) {
        buttons[index].textContent = suggestion.substring(2);
        buttons[index].addEventListener("click", (event) => {
          const suggestionText = event.target.textContent;
          sendQuery(
            suggestionText,
            sessionId,
            roomId,
            document.getElementById("friendly-name").value,
          );
        });
      }
    });
  } catch (error) {
    console.error("Error updating suggestions:", error);
  }
}
