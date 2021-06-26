const socket = io(`${document.location.protocol === 'https:' ? 'wss' : 'ws'}://${document.location.host}`);
const favicon = new Favico({
  animation: 'popFade'
});

var nbNotif = $('#notifContent > .notif').length;;

function updateNotif() {
  nbNotif = $('#notifContent > .notif').length;
  if (nbNotif > 0) {
    favicon.badge(nbNotif);
    $('#nbNotif').css({
      'display': "block"
    });
    $('#nbNotif').html(nbNotif);
    $('#noNotif').css({
      'display': "none"
    });
    $('#toutLu').css({
      'display': "block"
    });
  } else {
    favicon.reset();
    $('#nbNotif').css({
      'display': "none"
    });
    $('#noNotif').css({
      'display': "block"
    });
    $('#toutLu').css({
      'display': "none"
    });
  }
}

function supprNotif(id) {
  socket.emit('supprNotif', id);
  $('#' + id).remove();
  updateNotif();
}

function allSuppr() {
  $('#notifContent > .notif').each(function() {
    supprNotif($(this).attr('id'));
  });
}

updateNotif();

socket.on('connect', function() {
  socket.emit('connectToNotif');
});

socket.on('notif', (html) => {
  $('#notifContent').append(html);
  updateNotif();
});

socket.on('newNotif', (html) => {
  $('#notifContent').append(html);
  updateNotif();
  $.playSound('/static/sounds/notif.mp3');
});
