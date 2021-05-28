function supprimer(e) {
  e.preventDefault();
  var id = document.getElementById('idSupprimé').value;
  var donnees = $('#supprForm').serialize();
  $.ajax({
    url: '/administration/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      document.getElementById('divDemande'+id).style.display='None';
      supprimerClose();
    },
  });
}

function suppression(id){
  document.getElementById("idSupprimé").value = id;
  supprimerOpen();
}

function supprimerOpen(){
  $("#suppression").addClass("is-active");
}

function supprimerClose(){
  $("#suppression").removeClass("is-active");
}

function valider(e) {
  e.preventDefault();
  var id = document.getElementById('idValidé').value;
  var donnees = $('#valForm').serialize();
  $.ajax({
    url: '/administration/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      document.getElementById('divDemande'+id).style.display='None';
      validerClose();
    },
  });
}

function validation(id){
  document.getElementById("idValidé").value = id;
  validerOpen();
}

function validerOpen(){
  $("#validation").addClass("is-active");
}

function validerClose(){
  $("#validation").removeClass("is-active");
}
