const sender_id = JSON.parse(document.getElementById("sender-id").textContent);
const receiver_id = JSON.parse(
  document.getElementById("receiver-id").textContent
);

let loc = window.location;

let wsStart = "ws://";

if (loc.protocol === "https") {
  wsStart = "wss://";
}

let endpoint = wsStart + loc.host + loc.pathname;

var socket = new WebSocket(endpoint);

let chat_form = $("#chat-form");
let chat_input = $("#chat-input");
let chat_body = $("#chat-body");

socket.onopen = function (e) {
  console.log(
    `Connection to user-${receiver_id} opened by user-${sender_id}`,
    e
  );
};

socket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  if (data.receiver == receiver_id) {
    chat_body.innerHTML += `
    <tr class="px-4 py-2 mb-4 bg-purple-950 text-white text-left rounded-md flex flex-col max-w-md float-left">
      <td>
        <p>${data.message}</p>
        <span class="text-xs text-gray-400">${data.timestamp}, today</span>
      </td>
    </tr>
    `;
  } else {
    chat_body.innerHTML += `
    <tr class="px-4 py-2 mb-4 bg-amber-100 text-black text-right rounded-md flex flex-col max-w-md float-right">    
      <td>
        <p>${data.message}</p>
        <span class="text-xs text-gray-400">${data.timestamp}, today</span>
      </td>
    </tr>
    `;
  }
  console.log(data);
};

socket.onerror = function (e) {
  console.log("Connection error", e);
};

socket.onclose = function (e) {
  console.log("Connection closed", e);
};

chat_form.on("submit", function (e) {
  e.preventDefault();
  let chat_message = chat_input.val();
  let data = JSON.stringify({
    message: chat_message,
    receiver: receiver_id,
  });

  socket.send(data);
  $(this)[0].reset();
});

function toggleDropdown(e) {
  e.name === "dropdownBtn"
    ? ((e.name = "close"), dropdownMenu.classList.remove("hidden"))
    : ((e.name = "dropdownBtn"), dropdownMenu.classList.add("hidden"));
}
