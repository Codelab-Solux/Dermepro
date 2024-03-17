var { textContent: user_id } = document.getElementById("user_id");
console.log("User ID:", user_id);

var endpoint = `/ws/notifications/`;
var notifierSocket = new WebSocket("ws://" + window.location.host + endpoint);

notifierSocket.onopen = function () {
  console.log("WebSocket connected to " + endpoint);
};

notifierSocket.onmessage = function (event) {
  var data = JSON.parse(event.data);
  notify(data); // Update content based on received data
};

notifierSocket.onclose = function () {
  console.log("WebSocket disconnected from " + endpoint);
};

notifierSocket.onerror = function (error) {
  console.error("WebSocket error:", error);
};

function notify(data) {
  // Increment the value in the notification counter by 1
  let new_notification;
  var notificationCounter = document.getElementById("notif_counter");
  var notificationList = document.getElementById("notif_list");
  notificationCounter.classList.remove("hidden");
  var currentCount = parseInt(notificationCounter.textContent);
  if (!isNaN(currentCount)) {
    notificationCounter.textContent = currentCount + 1;
  } else {
    notificationCounter.textContent = 1;
  }
  // Display an alert with information about the received notification
  // alert(`Notification type : ${data.type}`);

  function get_sex_title(data) {
      if( data.sex === "male")
      { return "M."} 
      else 
      { return "Mme."}
    }

  if (data.type === "chat") {
    new_notification = `<li
        hx-select="#base"
        hx-get="{% url 'chats' %}"
        hx-swap="innerHTML"
        hx-trigger="click"
        id="notif${data.id}"
        class="notif_card w-full px-3 py-2 bg-white rounded-md border cursor-pointer flex gap-2 items-center"
      >
        <i class="mr-2 fa-solid fa-envelope mr-2"></i>
        <article class="grid gap-1">
          <b>${data.sender}</b>
          <p>${data.message.slice(0, 10) + "..."}</p>
        </article>
      </li>
    `;
  } 
  else if (data.type === "visit") {
    new_notification = `<li
        hx-select="#base"
        hx-target="#base"
        hx-get="{% url 'visits' %}"
        hx-swap="innerHTML"
        hx-trigger="click"
        id="notif${data.id}"
        class="notif_card w-full px-3 py-2 bg-white rounded-md border cursor-pointer grid gap-2 items-center"
      >
        <span><i class="mr-2 fa-solid fa-user-tie mr-2"></i>Nouvelle visite de </span
        > <b>${get_sex_title(data)} ${data.person};
        </b>
      </li>`;
  } 
  else if (data.type === "appointment") {
    new_notification = `<li
        hx-select="#base"
        hx-get="{% url 'appointments' %}"
        hx-swap="innerHTML"
        hx-trigger="click"
        id="notif${data.id}"
        class="notif_card w-full px-3 py-2 bg-white rounded-md border cursor-pointer grid gap-2 items-center"
        >
        <span><i class="mr-2 fa-solid fa-user-tie mr-2"></i>Nouveau rendez-vous avec </span>
        <b>${get_sex_title(data)} ${data.person};
        </b>
      </li>`;
  } 
  else {
    new_notification = `
    <li
      id="notif${data.id}"
      class="notif_card w-full px-3 py-2 bg-white rounded-md border cursor-pointer grid gap-2 items-center"
    >
      <span><i class="mr-2 fa-solid fa-question mr-2"></i>Notification anonym </span>
    </li>
    `;
  }

  // alert(new_notification);
  // notificationList.insertAdjacentHTML("beforeend", new_notification);
  notificationList.appendChild(
    document.createRange().createContextualFragment(new_notification)
  );

}
