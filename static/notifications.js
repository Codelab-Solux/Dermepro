const active_user_id = JSON.parse(
  document.getElementById("active_user_id").textContent
);
const notification_socket = new WebSocket(
  `ws://${window.location.host}/notifications/`
);

console.log(active_user_id);

var notifier = $("#notifier");
var has_notification;

notification_socket.onopen = function (e) {
  console.log("Notifying now - - -");
};

notification_socket.onerror = function (e) {
  console.log("Notification error !!!");
};

notification_socket.onmessage = function (e) {
  console.log("Notification received -/-");
  const data = JSON.parse(e.data);
  if (data.notification_count > 0) {
    has_notification = true;
    console.log("has_notification", has_notification);
    notifier.classList.remove("hidden");
  } else {
    has_notification = false;
    console.log("has_notification", has_notification);
    notifier.classList.add("hidden");
  }
};

notification_socket.onclose = function (e) {
  console.log("Notification closed -/-");
};
