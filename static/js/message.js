$(document).ready(function() {
  $('#titreetmsg').css({
    height: (70 / 100 * ($(window).height())).toString() + 'px',
    width: (85 / 100 * ($(window).width())).toString() + 'px',
  });
  $('#nomgroupe').css({
    height: (80 / 100 * ($(window).height())).toString() + 'px',
  });
});

function divnewgroupopen(){
  $(".modal").addClass("is-active");
}
function divnewgroupclose(e){
  $(".modal").removeClass("is-active");
}

function envoi(e) {
  e.preventDefault();
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

function supprimer(e) {
  e.preventDefault();
  var donnees = $('#suppressionMsg').serialize();
  $.ajax({
    url: '/suppressionMsg/',
    type: "POST",
    data: donnees,
    success: function(response) {
      $('#suppressionMsg').trigger("reset");
    },
  });
}

function reponseMsg(nb){
  var idMsg = document.getElementById('id'+nb).value;
  var contentMsg = document.getElementById('contenu'+nb).value;
  repmsg = document.getElementById('messageForm');
  repmsg.insertAdjacentHTML('beforebegin',contentMsg);
  document.getElementById('reponse').value = idMsg;
}
