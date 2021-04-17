$(document).ready(function() {
  $('#titreetmsg').css({
    height: (80 / 100 * ($(window).height())).toString() + 'px',
    width: (85 / 100 * ($(window).width())).toString() + 'px',
  });
  $('#nomgroupe').css({
    height: (80 / 100 * ($(window).height())).toString() + 'px',
  });
  $('#listeuser').css({
    height: (40 / 100 * ($(window).height())).toString() + 'px',
  });
  searchUser();
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
  enleverRep();
}

function searchUser() {
  var recherche = $('#searchUser').val();
  $.ajax({
    url: '/searchUser_newgroup/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: {
      'search': recherche
    }, // et on envoie nos données
    success: function(response) {
      $('#listeuser').html(response);
    },
  });
}

$('#searchUser').keyup(function() {
  console.log('hello');
  searchUser();
});

// function supprimer(e) { ne sert plus pour le moment
//   e.preventDefault();
//   var donnees = $('#suppressionMsg').serialize();
//   $.ajax({
//     url: '/suppressionMsg/',
//     type: "POST",
//     data: donnees,
//     success: function(response) {
//       $('#suppressionMsg').trigger("reset");
//     },
//   });
// }

$('#inputMsg').focus();
const messages = document.getElementById('messages');
// messages.scrollTop = messages.scrollHeight;

var start = new Date();

function refresh() {
  var dernierID = $('#messages div[id]:last').attr('id'); // on récupère l'id le plus récent
  var idGroupe = $('[name="group"]').attr("value");
  if (dernierID === undefined) {
    dernierID = start.toISOString();
  }
  $.ajax({
    url: "/refreshMsg/",
    type: "GET",
    data: "idMsg=" + dernierID + '&idgroupe=' + idGroupe, // et on envoie nos données
    success: function(html) {
      $('#messages').append(html); // on veut ajouter les nouveaux messages au début du bloc #messages
      // messages.scrollTop = messages.scrollHeight;
    }
  });
}

setInterval(refresh, 1000);

function reponseMsg(nb) {
  var contentMsg = document.getElementById('contenu' + nb).value;
  repmsg = document.getElementById('messageForm');
  document.getElementById('champReponse').innerHTML = contentMsg;
  // document.getElementById('buttonRep').style.display = block;
  document.getElementById('reponse').value = nb;
  idMsg = "None";
  contentMsg = "";
}

function enleverRep() {
  document.getElementById('champReponse').innerHTML = "";
  // document.getElementById('buttonRep').style.display = none;
  document.getElementById('reponse').value = "None";
}
