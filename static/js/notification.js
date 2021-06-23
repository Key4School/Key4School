const socket = io(`${document.location.protocol === 'https:' ? 'wss' : 'ws'}://${document.location.host}`);

const favicon = new Favico({
  animation: 'popFade',
  position: 'down'
});
let nbNotifs = $('#notifContent > .notif').length;;

function updateNotif() {
  if (nbNotifs > 0) {
    $('#nbNotif').css({
      'display': "block"
    });
    $('#nbNotif').html(nbNotifs);
    $('#noNotif').css({
      'display': "none"
    });
    $('#toutLu').css({
      'display': "block"
    });
  } else {
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

  favicon.badge(nbNotifs);
}

function supprNotif(id) {
  socket.emit('supprNotif', id);
  $('#' + id).remove();
  nbNotifs--;
  updateNotif();
}

function allSuppr() {
  $('#notifContent > .notif').each(function() {
    supprNotif($(this).attr('id'));
  });

  nbNotifs = 0;
}

updateNotif();

socket.on('connect', function() {
  socket.emit('connectToNotif');
});

socket.on('newNotif', (html) => {
  $('#notifContent').append(html);
  nbNotifs++;
  updateNotif();
});