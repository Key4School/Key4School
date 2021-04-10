function envoi(){
  var donnees = $('#messageForm').serialize();
  $.ajax({
    url: '/messages', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      $('#messageForm').trigger("reset");
    },
  });
}
