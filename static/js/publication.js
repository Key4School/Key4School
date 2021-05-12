function like(id){
  selectionlike = document.getElementById("like_"+id).className
  if (selectionlike == "far fa-thumbs-up") {
    document.getElementById("like_"+id).className = "fas fa-thumbs-up";
    document.getElementById("like_"+id).innerHTML = parseInt(document.getElementById("like_"+id).innerHTML) + 1; // on ajoute 1 au nb de likes

  }
  if (selectionlike == "fas fa-thumbs-up"){
    document.getElementById("like_"+id).className = "far fa-thumbs-up";
    document.getElementById("like_"+id).innerHTML = parseInt(document.getElementById("like_"+id).innerHTML) - 1; // on enlève 1 au nb de likes
  }

  fetch(`likePost/${id}`, {
    method: 'post',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  });
}


function sign(id){
  selectionlike = document.getElementById("sign_"+id).className
  if (selectionlike == "far fa-flag") {
    document.getElementById("idSignalé").value = id;
    signalisationOpen();
    document.getElementById("sign_"+id).className = "fas fa-flag";

  }
  if (selectionlike == "fas fa-flag"){
    document.getElementById("sign_"+id).className = "far fa-flag";
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
    },
  });
}
