

//  tabs control ----------------------------------------------------------------------------------------------------
document.getElementById("defaultTab").click();
function openTab(event, tabName) {
  var i, tabcontent, tabBtn;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tabBtn = document.getElementsByClassName("tabBtn");
  for (i = 0; i < tabBtn.length; i++) {
    tabBtn[i].className = tabBtn[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "block";
  event.currentTarget.className += " active";
  var minitabs = document.getElementsByClassName("minitabcontent");
  if (minitabs.length != 0) {
    minitabs = tabcontent.children;
  }
}
