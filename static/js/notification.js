const socket = io(`ws://${document.location.host}`);

function updateNotif(){
  var nbNotif = document.querySelectorAll('#notifContent > .notif').length;
  if (nbNotif > 0) {
    document.getElementById('nbNotif').style.display = "block";
    document.getElementById('nbNotif').innerHTML = nbNotif;
    document.getElementById('noNotif').style.display = "none";
  } else {
    document.getElementById('nbNotif').style.display = "none";
    document.getElementById('noNotif').style.display = "block";
  }
}

function supprNotif(id){
  socket.emit('supprNotif', id);
  document.getElementById(id).remove();
  updateNotif();
}

updateNotif();

socket.on('connect', function() {
  socket.emit('connectToNotif');
});

socket.on('newNotif', (html) => {
  document.getElementById('notifContent').innerHTML += html;
  updateNotif();
});
