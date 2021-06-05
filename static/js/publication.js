var id;

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

  fetch(`/likePost/${id}`, {
    method: 'post',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  });
}

function like_rep(idMsg, idRep){
  selectionlike = document.getElementById("like_"+idRep).className
  if (selectionlike == "far fa-thumbs-up") {
    document.getElementById("like_"+idRep).className = "fas fa-thumbs-up";
    document.getElementById("like_"+idRep).innerHTML = parseInt(document.getElementById("like_"+idRep).innerHTML) + 1; // on ajoute 1 au nb de likes

  }
  if (selectionlike == "fas fa-thumbs-up"){
    document.getElementById("like_"+idRep).className = "far fa-thumbs-up";
    document.getElementById("like_"+idRep).innerHTML = parseInt(document.getElementById("like_"+idRep).innerHTML) - 1; // on enlève 1 au nb de likes
  }

  fetch(`/likeRep/${idMsg}/${idRep}`, {
    method: 'post',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  });
}


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

function resoudre(idMsg) {
  fetch(`/resoudre/${idMsg}`, {
    method: 'post',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  })
    .then((res) => {
      window.location.reload(true);
    });
}