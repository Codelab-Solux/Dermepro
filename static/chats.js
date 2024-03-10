var sender_id = JSON.parse(document.getElementById("curr_user").textContent);
var receiver_id = JSON.parse(document.getElementById("other_user").textContent);

// let loc = window.location;

// let wsStart = "ws://";

// if (loc.protocol === "https") {
//   wsStart = "wss://";
// }

// let endpoint = wsStart + loc.host + loc.pathname;

// var chatSocket = new WebSocket(endpoint);
var chatSocket = new WebSocket(
  `ws://${window.location.host}/chats/threads/${receiver_id}/`
);

let chat_form = $(`#chat_form`);
let chat_input = $("#chat-input");
var chat_body = $("#chat-box");

chatSocket.onopen = function (e) {
  alert(e);
  // console.log(
  //   `Connection to user-${receiver_id} opened by user-${sender_id}`,
  //   e
  // );

  // chat_body.append(`<div> Textons nous vivant </div>`);
};

chatSocket.onmessage = function (e) {
  let chat_div;
  var currentdate = new Date();
  let time = currentdate.getHours() + ":" + currentdate.getMinutes();
  const data = JSON.parse(e.data);
  if (data.receiver != receiver_id) {
    chat_div = `
    <tr class="max-h-20">    
      <td class="px-4 py-2 bg-amber-100 text-black text-left rounded-md flex flex-col max-w-md float-left">
        <p>${data.message}</p>
        <span class="text-xs text-gray-500 text-left">${time}, today</span>
      </td>
    </tr>
    `;
  } else {
    chat_div = `
    <tr class="max-h-20">
      <td  class="px-4 py-2 bg-purple-950 text-white text-right rounded-md flex flex-col max-w-md float-right">
        <p>${data.message}</p>
        <span class="text-xs text-gray-300 text-right">${time}, today</span>
      </td>
    </tr>
    `;
  }
  console.log(data.message, time);

  chat_body.append($(chat_div));
  chat_body.animate(
    {
      scrollTop: $(chat_body).height(),
    },
    100
  );
};

chatSocket.onerror = function (e) {
  console.log("Connection error", e);
};

chatSocket.onclose = function (e) {
  console.log("Connection closed", e);
};

chat_form.on("submit", function (e) {
  e.preventDefault();
  let chat_message = chat_input.val();
  let data = JSON.stringify({
    message: chat_message,
    receiver: receiver_id,
    sender: sender_id,
  });

  chatSocket.send(data);
  $(this)[0].reset();
});

function toggleDropdown(e) {
  e.name === "dropdownBtn"
    ? ((e.name = "close"), dropdownMenu.classList.remove("hidden"))
    : ((e.name = "dropdownBtn"), dropdownMenu.classList.add("hidden"));
}
