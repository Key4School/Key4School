function input(type){
  if($('#'+ type)!==undefined){
    var contenu= $('#'+ type).html().trim(); // renvoie le texte contenu à l'intérieur du paragraphe
    if (!contenu.includes('Non-renseigné')){
      $('#content' + type).html('<input onfocus="this.select();" onclick="this.select();" class="input" name="'+type+'" id="input'+type+'" type="text" value="'+ contenu + '"/>'); // remplace le code HTML actuel par celui-ci
    }else{
      $('#content' + type).html('<input onfocus="this.select();" onclick="this.select();" class="input" name="'+type+'" id="input'+type+'" type="text" placeholder="Non-renseigné"/>'); // remplace le code HTML actuel par celui-ci
    }
  }
}

function updateImgOpen() {
  $("#replaceImg").addClass("is-active");
}

function updateImgClose() {
  $("#replaceImg").removeClass("is-active");
}

function signalisationProfil(){
  selectionSign = document.getElementById("signProfil").className
  if (selectionSign == "far fa-flag") {
    signalisationProfilOpen();


  }
  if (selectionSign == "fas fa-flag"){
    designalisationProfilOpen();
  }
}

function signalisationProfilOpen() {
  $("#signalisationProfil").addClass("is-active");
}

function signalisationProfilClose() {
  $("#signalisationProfil").removeClass("is-active");
}

function designalisationProfilOpen() {
  $("#designalisationProfil").addClass("is-active");
}

function designalisationProfilClose() {
  $("#designalisationProfil").removeClass("is-active");
}

function signalerProfil(e) {
  e.preventDefault();
  var donnees = $('#signalementProfil').serialize();
  $.ajax({
    url: '/signPostProfil/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      $('#signalementProfil').trigger("reset");
      signalisationProfilClose();
      document.getElementById("signProfil").className = "fas fa-flag";
    },
  });
}

function designalerProfil(e) {
  e.preventDefault();
  var donnees = $('#signalementProfil').serialize();
  $.ajax({
    url: '/signPostProfil/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      designalisationProfilClose();
      document.getElementById("signProfil").className = "far fa-flag";
    },
  });
}

function divsubjectopen() {
  var donnees = $('#updateProfil').serialize();
  $.ajax({
    url: '/updateprofile/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      $("#subjects").addClass("is-active");
    },
  });
}

function divsubjectclose(e) {
  $("#subjects").removeClass("is-active");
}
