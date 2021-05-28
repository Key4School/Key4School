function supprimer(e,a) {
  e.preventDefault();
  var donnees = $('#demandeSuppr'+a).serialize();
  $.ajax({
    url: '/administration/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function() {
        testONLBN();
    },
  });
}

function valider(e) {
  e.preventDefault();
  var donnees = $('#demandeValider'+a).serialize();
  $.ajax({
    url: '/administration/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
       testONLBN();
    },
  });
}

testONLBN(){
  document.getElementById('divTest').innerHTML='yass';
}
