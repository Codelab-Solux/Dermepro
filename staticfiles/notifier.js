var { textContent: user_id } = document.getElementById("user_id");
console.log("User ID:", user_id);

// Function to get the appropriate WebSocket URL based on the current page protocol
function getWebSocketURL() {
  var protocol = window.location.protocol.startsWith("https")
    ? "wss://"
    : "ws://";
  return protocol + window.location.host + `/ws/notifications/`;
}

var endpoint = getWebSocketURL();
var notifierSocket = new WebSocket(endpoint);

notifierSocket.onopen = function () {
  console.log("WebSocket connected to " + endpoint);
};

notifierSocket.onmessage = function (event) {
  var data = JSON.parse(event.data);
  // notify(data);

  updateUI(data); // Update content based on received data
};

notifierSocket.onclose = function () {
  console.log("WebSocket disconnected from " + endpoint);
};

notifierSocket.onerror = function (error) {
  console.error("WebSocket error:", error);
};

let path = window.location.pathname;

// Reload thread list by triggering a request to fetch updated content
function updateUI(data) {
  // alert('new notification')
  document.getElementById("badge_reloader").click();

  if (data.type === "chat" && path === "/chats/") {
    document.getElementById("chats_reloader").click();
  } else if (data.type === "user" && path === "/users/") {
    document.getElementById("users_reloader").click();
  } else if (data.type === "status_quo") {
    // alert('status quo changed')
    document.getElementById("status_quo_reloader").click();
  } else if (data.type === "visit" && path === "/visits/") {
    document.getElementById("visits_reloader").click();
  } else if (data.type === "visits_status") {
    document.getElementById("visits_status_reloader").click();
  } else if (data.type === "appointment" && path === "/appointments/") {
    document.getElementById("appointments_reloader").click();
  } else if (data.type === "appointments_status") {
    document.getElementById("appointments_status_reloader").click();
  }
}
