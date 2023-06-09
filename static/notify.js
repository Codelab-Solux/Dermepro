const notify_socket = new WebSocket(`ws://${window.location.host}/notify/`);

notify_socket.onopen = function (e) {
  console.log("Notifying now - - -");
};
notify_socket.onerror = function (e) {
  console.log("Notification error !!!");
};
notify_socket.onclose = function (e) {
  console.log("Notification closed -/-");
};
