const socket = io(`ws://${document.location.host}`);
var nbNotif = document.querySelectorAll('#notifContent > .notif').length;
if (nbNotif > 0) {
  document.getElementById('nbNotif').style.display = "block";
  document.getElementById('nbNotif').innerHTML = nbNotif;
} else {
  document.getElementById('nbNotif').style.display = "none";
}

socket.on('connect', function() {
  socket.emit('connectToNotif');
});

socket.on('newNotif', (html) => {
  document.getElementById('notifContent').innerHTML += html;
  var nbNotif = document.querySelectorAll('#notifContent > .notif').length;
  if (nbNotif > 0) {
    document.getElementById('nbNotif').style.display = "block";
    document.getElementById('nbNotif').innerHTML = nbNotif;
  } else {
    document.getElementById('nbNotif').style.display = "none";
  }
});
