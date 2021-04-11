$(document).ready(function() {
  $('#titreetmsg').css({
      height: (80 / 100 * ($(window).height())).toString() + 'px',
      width: (75 / 100 * ($(window).width())).toString() + 'px',
    });
  function envoi(){
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
});
