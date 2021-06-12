var socket = io(`ws://${document.location.host}`);

socket.on('connect', function() {
  socket.emit('connectToNotif');
});
