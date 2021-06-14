const socket = io(`ws://${document.location.host}`);
const nbNotifElem = document.getElementById('nbNotif');
const noNotif = document.getElementById('noNotif');
const toutLu = document.getElementById('toutLu');
const notifContent = document.getElementById('notifContent');

function updateNotif() {
  var nbNotif = document.querySelectorAll('#notifContent > .notif').length;
  if (nbNotif > 0) {
    nbNotifElem.style.display = "block";
    nbNotifElem.innerHTML = nbNotif;
    noNotif.style.display = "none";
    toutLu.style.display = "block";
  } else {
    nbNotifElem.style.display = "none";
    noNotif.style.display = "block";
    toutLu.style.display = "none";
  }
}

function supprNotif(id) {
  socket.emit('supprNotif', id);
  document.getElementById(id).remove();
  updateNotif();
}

function allSuppr() {
  var notifications = document.querySelectorAll('#notifContent > .notif');
  for (const notification of notifications) {
    supprNotif(notification.id);
  }
}

updateNotif();

socket.on('connect', function() {
  socket.emit('connectToNotif');
});

socket.on('newNotif', (html) => {
  notifContent.innerHTML += html;
  updateNotif();
});
