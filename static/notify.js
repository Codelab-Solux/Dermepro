const notify_socket = new WebSocket(`ws://${window.location.host}/notify/`);

var notifier = $("#notifier");
var has_notification;

notify_socket.onopen = function (e) {
  console.log("Notifying now - - -");
};

notify_socket.onerror = function (e) {
  console.log("Notification error !!!");
};

notify_socket.onmessage = function (e) {
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

notify_socket.onclose = function (e) {
  console.log("Notification closed -/-");
};
