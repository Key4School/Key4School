$(document).ready(function() {
  $('#titreetmsg').css({
      height: (80 / 100 * ($(window).height())).toString() + 'px',
      width: (85 / 100 * ($(window).width())).toString() + 'px',
    });
    $('#nomgroupe').css({
        height: (90 / 100 * ($(window).height())).toString() + 'px',
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
        }
      }
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
