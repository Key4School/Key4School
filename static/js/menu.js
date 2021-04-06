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
  }
}
