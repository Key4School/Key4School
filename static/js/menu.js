$(document).ready(function() {
  $('#multichoix').css({
    height: (100 / 100 * ($(window).height())).toString() + 'px',
    top: (10 / 100 * ($(window).height())).toString() + 'px',
  });
  $('#notif').css({
    height: (100 / 100 * ($(window).height())).toString() + 'px',
    top: (10  / 100 * ($(window).height())).toString() + 'px',
  });
});
function divmenu() {
  if ($('#multichoix').css("display") == 'none') {
    $('#multichoix').css({
      display: "block",
    });
    $('#page').append('<div id="filtre" onclick="divmenu()" style="opacity:0;"><div>');
  } else {
    $('#multichoix').css({
      display: "none",
    });
    $('#filtre').remove();
  }
}
function divnotif() {
  if ($('#notif').css("display") == 'none') {
    $('#notif').css({
      display: "block",
    });
    $('#page').append('<div id="filtre" onclick="divnotif()" style="opacity:0;"><div>');
  } else {
    $('#notif').css({
      display: "none",
    });
    $('#filtre').remove();
  }
}
