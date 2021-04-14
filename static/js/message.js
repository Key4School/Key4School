$(document).ready(function() {
  $('#titreetmsg').css({
    height: (80 / 100 * ($(window).height())).toString() + 'px',
    width: (75 / 100 * ($(window).width())).toString() + 'px',
  });
  $('#nomgroupe').css({
    height: (80 / 100 * ($(window).height())).toString() + 'px',
  });
});

function divnewgroupopen() {
  $("#newgrou").addClass("is-active");
}

function divnewgroupclose(e) {
  $("#newgrou").removeClass("is-active");
}

function divoptionopen() {
  $("#option").addClass("is-active");
}

function divoptionclose(e) {
  $("#option").removeClass("is-active");
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


$('[name="contenuMessage"]').focus();
const messages = document.querySelector('.messages');
messages.scrollTop = messages.scrollHeight;

function reponseMsg(nb){
  var idMsg = document.getElementById('id'+nb).value;
  var contentMsg = document.getElementById('contenu'+nb).value;
  repmsg = document.getElementById('messageForm');
  repmsg.insertAdjacentHTML('beforebegin',contentMsg);
  document.getElementById('reponse').value = idMsg;
}

function refresh() {
  var dernierID = $('.messages div[id]:last').attr('id'); // on récupère l'id le plus récent
  var idGroupe=$('[name="group"]').attr("value");
  $.ajax({
    url: "/refreshMsg/",
    type: "GET",
    data: "idMsg=" + dernierID + '&idgroupe=' + idGroupe, // et on envoie nos données
    success: function(html) {
      $('.messages').append(html); // on veut ajouter les nouveaux messages au début du bloc #messages
      messages.scrollTop = messages.scrollHeight;
    }
  });
}

setInterval(refresh, 1000);
