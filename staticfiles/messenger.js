var { textContent: thread_id } = document.getElementById("thread_id");
var { textContent: sender_id } = document.getElementById("curr_user_id");
var { textContent: receiver_id } = document.getElementById("other_user_id");
var chat_box = document.getElementById(`chat_box_${thread_id}`);
var chat_form = document.getElementById(`chat_form_${thread_id}`);

// Function to get the appropriate WebSocket URL based on the current page protocol
function getWebSocketURL() {
  var protocol = window.location.protocol.startsWith("https")
    ? "wss://"
    : "ws://";
  return protocol + window.location.host + `/ws/chats/threads/${receiver_id}/`;
}

var endpoint = getWebSocketURL();
var messengerSocket = new WebSocket(endpoint);

messengerSocket.onopen = () => {
  console.log("WebSocket connected to " + endpoint);
};

messengerSocket.onmessage = (event) => {
  var currentdate = new Date();
  var curr_time = `${currentdate.getHours()}:${currentdate.getMinutes()}`;
  var data = JSON.parse(event.data);

  let new_message;
  if (data.sender === sender_id) {
    new_message = `
    <tr class="max-h-16">
        <td class="mr-2 px-4 py-2 bg-purple-200 text-black text-right rounded-lg flex flex-col max-w-md float-right">
        <p>${data.message}</p>
          <small class="text-xs text-gray-500 text-right">${curr_time}</small>
        </td>
      </tr>`;
  } else {
    new_message = `
      <tr class="max-h-16">    
      <td class="px-4 py-2 bg-amber-200 text-black text-left rounded-lg flex flex-col max-w-md float-left">
      <p>${data.message}</p>
      <small class="text-xs text-gray-500 text-left">${curr_time}</small>
      </td>
      </tr>`;
  }

  chat_box.insertAdjacentHTML("beforeend", new_message);
  scrollToBottom();
  updateUI();
};

messengerSocket.onclose = () => {
  console.log("WebSocket disconnected from " + endpoint);
};

chat_form.addEventListener("submit", (event) => {
  event.preventDefault();
  var chat_input = document.getElementById("chat_input");
  var message = chat_input.value.trim();
  if (message !== "") {
    var data = JSON.stringify({
      type: "chat",
      thread_id,
      sender: sender_id,
      receiver: receiver_id,
      message: message,
    });
    messengerSocket.send(data);
    chat_input.value = "";
  }
});

// Function to scroll the conversation box to the bottom
function scrollToBottom() {
  $("#convo_box").animate(
    {
      scrollTop: $("#convo_box")[0].scrollHeight,
    },
    "slow"
  );
}

// Reload thread list by triggering a request to fetch updated content
function updateUI() {
  document.getElementById("chats_reloader").click();
}
