// const nested = require("json-server/lib/server/router/nested");

let loc = window.location;

let wsStart = "ws://";

if (loc.protocol === "https") {
  wsStart = "wss://";
}

let endpoint = wsStart + loc.host + loc.pathname;

var socket = new WebSocket(endpoint);

let input_message = $("#texto");
let message_body = $("#convo");
let messenger = $("#messenger");
const userID = $("#curr_user").val();

socket.onopen = async function (e) {
  console.log("Connection opened by user: ", userID, e);
  messenger.on("submit", function (e) {
    e.preventDefault();
    let text_message = input_message.val();
    let send_to = get_active_other_user_id();
    let thread_id = get_active_thread_id();

    let data = {
      message: text_message,
      sent_by: userID,
      send_to: send_to,
      thread_id: thread_id,
    };
    data = JSON.stringify(data);
    socket.send(data);
    $(this)[0].reset();
  });
};

socket.onmessage = async function (e) {
  console.log("Connection message", e);
  let data = JSON.parse(e.data);
  let message = data["message"];
  let sent_by_id = data["sent_by"];
  let thread_id = data["thread_id"];
  newMessage(message, sent_by_id, thread_id);
};

socket.onerror = async function (e) {
  console.log("Connection error", e);
};

socket.onclose = async function (e) {
  console.log("Connection closed", e);
};

function newMessage(message, sent_by_id, thread_id) {
  // if ($.trim(message) === "") {
  //   console.log("no  message");
  //   // return false;
  // }
  let message_element;
  let chat_id = "chat_" + thread_id;
  var currentdate = new Date();
  let time = currentdate.getHours() + ":" + currentdate.getMinutes();
  message_element = `
          <p>${message}</p>
    `;

  // if (sent_by_id === userID) {
  //   message_element = `
  //       <div class="msg_out px-4 py-2 mb-4 text-black text-right rounded-xl flex flex-col max-w-md">
  //         <p>${message}</p>
  //         <span class="text-xs text-gray-400">${time}, today</span>
  //       </div>
  //   `;
  // } else {
  //   message_element = `
  //       <div class="msg_in px-4 py-2 mb-4 text-white text-left rounded-xl flex flex-col max-w-md">
  //         <p>${message}</p>
  //         <span class="text-xs text-gray-400">${time}, today</span>
  //       </div>
  //   `;
  // }

  message_body.append($(message_element));
  message_body.animate(
    {
      scrollTop: $(message_body).height(),
    },
    100
  );
  // input_message.val(null);
}

function toggleDropdown(e) {
  e.name === "dropdownBtn"
    ? ((e.name = "close"), dropdownMenu.classList.remove("hidden"))
    : ((e.name = "dropdownBtn"), dropdownMenu.classList.add("hidden"));
}

// $(".contact-li").on("click", function () {
//   $(".contacts .active").removeClass("active");
//   $(".contacts .active").addClass("bg-white");
//   $(this).addClass("active");

//   let chat_id = $(this).attr("chat-id");
//   $(".msg-box.visible").removeClass("visible");
//   $(`.msg-box[chat-id=${chat_id}]`).addClass("visible");
// });

function get_active_other_user_id() {
  let other_user_id = $(".msg-box").attr("other-user-id");
  other_user_id = $.trim(other_user_id);
  console.log("converser : ", other_user_id);
  return other_user_id;
}

function get_active_thread_id() {
  let chat_id = $(".msg-box").attr("chat-id");
  let thread_id = chat_id.replace("chat_", "");
  console.log("chat_id : ", thread_id);
  return thread_id;
}
