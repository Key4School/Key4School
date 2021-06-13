function supprimer(e) {
  e.preventDefault();
  var id = document.getElementById('idSupprimé').value;
  var donnees = $('#supprForm').serialize();
  $.ajax({
    url: '/administration/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      document.getElementById('divDemande_'+id).style.display='None';
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
      document.getElementById('divDemande_'+id).style.display='None';
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

function sanctionner(e) {
  e.preventDefault();
  var id = document.getElementById('idSanctionné').value;
  var donnees = $('#SancForm').serialize();
  $.ajax({
    url: '/sanction/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      $('#SancForm').trigger("reset");
      sanctionnerClose();
    },
  });
}

function sanction(){
  sanctionnerOpen();
}

function sanctionnerOpen(){
  $("#sanction").addClass("is-active");
}

function sanctionnerClose(){
  $("#sanction").removeClass("is-active");
}

function validerUser(e) {
  e.preventDefault();
  var donnees = $('#ValUserForm').serialize();
  $.ajax({
    url: '/administration/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      validerUserClose();
    },
  });
}

function validationUser(){
  validerUserOpen();
}

function validerUserOpen(){
  $("#validationUser").addClass("is-active");
}

function validerUserClose(){
  $("#validationUser").removeClass("is-active");
}

function supprimerRep(e) {
  e.preventDefault();
  var id = document.getElementById('idSupprimé').value;
  var donnees = $('#supprRepForm').serialize();
  $.ajax({
    url: '/administration/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      document.getElementById('divRep_'+id).style.display='None';
      supprimerRepClose();
    },
  });
}

function suppressionRep(id, idDemand){
  document.getElementById("idRepSupprimé").value = id;
  document.getElementById("idrepDemandSupprimé").value = idDemand;
  supprimerRepOpen();
}

function supprimerRepOpen(){
  $("#suppressionRep").addClass("is-active");
}

function supprimerRepClose(){
  $("#suppressionRep").removeClass("is-active");
}

function validerRep(e) {
  e.preventDefault();
  var id = document.getElementById('idRepValidé').value;
  var donnees = $('#valRepForm').serialize();
  $.ajax({
    url: '/administration/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      document.getElementById('divRep_'+id).style.display='None';
      validerRepClose();
    },
  });
}

function validationRep(id, idDemand){
  document.getElementById("idRepValidé").value = id;
  document.getElementById("idrepDemandValidé").value = idDemand;
  validerRepOpen();
}

function validerRepOpen(){
  $("#validationRep").addClass("is-active");
}

function validerRepClose(){
  $("#validationRep").removeClass("is-active");
}
