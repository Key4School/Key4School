$(document).ready(function() {
  $('#titreetmsg').css({
      height: (70 / 100 * ($(window).height())).toString() + 'px',
      width: (85 / 100 * ($(window).width())).toString() + 'px',
  });
  $('#nomgroupe').css({
      height: (80 / 100 * ($(window).height())).toString() + 'px',
  });
  function envoi(){
    if($('#envoimsg').val()!=''){
      var donnees = $('#messageForm').serialize();
      $.ajax({
        url: '/messages/', // on donne l'URL du fichier de traitement
        type: "POST", // la requête est de type POST
        data: donnees, // et on envoie nos données
        success: function(response) {
          $('#messageForm').trigger("reset");
        },
      });
    }
  }
});
function divnewgroup() {
  if ($('#newgroup').css("display") == 'none') {
    $('#newgroup').css({
      display: "block",
    });
    $('#page').append('<div id="filtre" onclick="divnewgroup()" style="opacity:0;"><div>');
  } else {
    $('#newgroup').css({
      display: "none",
    });
  }
}
