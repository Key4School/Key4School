const socket = io(`ws://${document.location.host}`);

socket.on('connect', function() {
  socket.emit('connectToNotif');
});

socket.on('newNotif', (html) => {
  document.getElementById('notifContent').innerHTML += html;
});
