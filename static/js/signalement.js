// profil
function signalisationProfil() {
  selectionSign = document.getElementById("signProfil").className
  if (selectionSign == "far fa-flag") {
    signalisationProfilOpen();


  }
  if (selectionSign == "fas fa-flag") {
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

// publications
function sign(rep){
  id=rep;
  selectionlike = document.getElementById("sign_"+id).className
  if (selectionlike == "far fa-flag") {
    document.getElementById("idSignalé").value = id;
    signalisationOpen();


  }
  if (selectionlike == "fas fa-flag"){
    document.getElementById("idDesignalé").value = id;
    designalisationOpen();
  }
}

function signalisationOpen() {
  $("#signalisation").addClass("is-active");
}

function signalisationClose() {
  $("#signalisation").removeClass("is-active");
}

function designalisationOpen() {
  $("#designalisation").addClass("is-active");
}

function designalisationClose() {
  $("#designalisation").removeClass("is-active");
}

function signaler(e) {
  e.preventDefault();
  var donnees = $('#signalement').serialize();
  $.ajax({
    url: '/signPost/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      $('#signalement').trigger("reset");
      signalisationClose();
      document.getElementById("sign_"+id).className = "fas fa-flag";
    },
  });
}

function designaler(e) {
  e.preventDefault();
  var donnees = $('#designalement').serialize();
  $.ajax({
    url: '/signPost/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      $('#designalement').trigger("reset");
      designalisationClose();
      document.getElementById("sign_"+id).className = "far fa-flag";
    },
  });
}

function sign_rep(rep){
  id=rep;
  selectionlike = document.getElementById("sign_"+id).className
  if (selectionlike == "far fa-flag") {
    document.getElementById("idRepSignalé").value = id;
    signalisationRepOpen();


  }
  if (selectionlike == "fas fa-flag"){
    document.getElementById("idRepDesignalé").value = id;
    designalisationRepOpen();
  }
}

function signalisationRepOpen() {
  $("#signalisationRep").addClass("is-active");
}

function signalisationRepClose() {
  $("#signalisationRep").removeClass("is-active");
}

function designalisationRepOpen() {
  $("#designalisationRep").addClass("is-active");
}

function designalisationRepClose() {
  $("#designalisationRep").removeClass("is-active");
}

function signalerRep(e) {
  e.preventDefault();
  var donnees = $('#signalementRep').serialize();
  $.ajax({
    url: '/signRepPost/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      $('#signalementRep').trigger("reset");
      signalisationRepClose();
      document.getElementById("sign_"+id).className = "fas fa-flag";
    },
  });
}

function designalerRep(e) {
  e.preventDefault();
  var donnees = $('#designalementRep').serialize();
  $.ajax({
    url: '/signRepPost/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      $('#designalementRep').trigger("reset");
      designalisationRepClose();
      document.getElementById("sign_"+id).className = "far fa-flag";
    },
  });
}

// messages
function signalisationDiscussion() {
  selectionSign = document.getElementById("sign").className
  if (selectionSign == "far fa-flag") {
    signalisationDiscussionOpen();
  }
  if (selectionSign == "fas fa-flag") {
    designalisationDiscussionOpen();
  }
}

function signalisationDiscussionClose() {
  $("#signalisationDiscussion").removeClass("is-active");
}

function signalisationDiscussionOpen() {
  $("#signalisationDiscussion").addClass("is-active");
}

function designalisationDiscussionClose() {
  $("#designalisationDiscussion").removeClass("is-active");
}

function designalisationDiscussionOpen() {
  $("#designalisationDiscussion").addClass("is-active");
}

function signalerDiscussion(e) {
  e.preventDefault();
  var donnees = $('#signalementDiscussion').serialize();
  $.ajax({
    url: '/signPostDiscussion/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      $('#signalementDiscussion').trigger("reset");
      signalisationDiscussionClose();
      document.getElementById("sign").className = "fas fa-flag";
    },
  });
}

function designalerDiscussion(e) {
  e.preventDefault();
  var donnees = $('#designalementDiscussion').serialize();
  $.ajax({
    url: '/signPostDiscussion/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      designalisationDiscussionClose();
      document.getElementById("sign").className = "far fa-flag";
    },
  });
}

var idMsg;
function signalisationMsg(idMsg) {
  selectionSignMsg = document.getElementById("signMsg_" + idMsg).className
  if (selectionSignMsg == "far fa-flag") {
    document.getElementById("idMsgSignalé").value = idMsg;
    signalisationMsgOpen();
  }
  if (selectionSignMsg == "fas fa-flag") {
    document.getElementById("idMsgDeSignalé").value = idMsg;
    designalisationMsgOpen();
  }
}

function signalisationMsgClose() {
  $("#signalisationMsg").removeClass("is-active");
}

function signalisationMsgOpen() {
  $("#signalisationMsg").addClass("is-active");
}

function designalisationMsgClose() {
  $("#designalisationMsg").removeClass("is-active");
}

function designalisationMsgOpen() {
  $("#designalisationMsg").addClass("is-active");
}

function signalerMsg(e) {
  e.preventDefault();
  var donnees = $('#signalementMsg').serialize();
  $.ajax({
    url: '/signPostMsg/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      signalisationMsgClose();
      idMsg = document.getElementById('idMsgSignalé').value;
      document.getElementById("signMsg_" + idMsg).className = "fas fa-flag";
      document.getElementById("sign").className = "fas fa-flag";
      $('#signalementMsg').trigger("reset");
    },
  });
}

function designalerMsg(e) {
  e.preventDefault();
  var donnees = $('#designalementMsg').serialize();
  $.ajax({
    url: '/signPostMsg/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      idMsg = document.getElementById('idMsgDeSignalé').value;
      document.getElementById("signMsg_" + idMsg).className = "far fa-flag";
      document.getElementById("sign").className = "far fa-flag";
      designalisationMsgClose();
    },
  });
}
