var id;

socket.on('connect', function() {
  return;
});

socket.on('newLike', (id_like) => {
  console.log('new');
  document.getElementById(`like_${id_like}`).innerHTML = parseInt(document.getElementById(`like_${id_like}`).innerHTML) + 1;
});

socket.on('removeLike', (id_like) => {
  console.log('remove');
  document.getElementById(`like_${id_like}`).innerHTML = parseInt(document.getElementById(`like_${id_like}`).innerHTML) - 1;
});

function like(id){
  selectionlike = document.getElementById(`like_${id}`).className
  if (selectionlike == "far fa-thumbs-up") {
    document.getElementById(`like_${id}`).className = "fas fa-thumbs-up";
    //document.getElementById(`like_${id}`).innerHTML = parseInt(document.getElementById(`like_${id}`).innerHTML) + 1; // on ajoute 1 au nb de likes
  }
  if (selectionlike == "fas fa-thumbs-up"){
    document.getElementById(`like_${id}`).className = "far fa-thumbs-up";
    //document.getElementById(`like_${id}`).innerHTML = parseInt(document.getElementById(`like_${id}`).innerHTML) - 1; // on enlève 1 au nb de likes
  }

  /*fetch(`/likePost/${id}`, {
    method: 'post',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  });*/

  socket.emit('postLike', {type: 'post', idPost: id});
}

function like_rep(idMsg, idRep){
  selectionlike = document.getElementById(`like_${idRep}`).className
  if (selectionlike == "far fa-thumbs-up") {
    document.getElementById(`like_${idRep}`).className = "fas fa-thumbs-up";
    //document.getElementById(`like_${idRep}`).innerHTML = parseInt(document.getElementById(`like_${idRep}`).innerHTML) + 1; // on ajoute 1 au nb de likes

  }
  if (selectionlike == "fas fa-thumbs-up"){
    document.getElementById(`like_${idRep}`).className = "far fa-thumbs-up";
    //document.getElementById(`like_${idRep}`).innerHTML = parseInt(document.getElementById(`like_${idRep}`).innerHTML) - 1; // on enlève 1 au nb de likes
  }

  /*fetch(`/likeRep/${idMsg}/${idRep}`, {
    method: 'post',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  });*/

  socket.emit('postLike', {type: 'rep', idPost: idMsg, idRep: idRep});
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
      document.getElementById("sign"+id).className = "fas fa-flag";
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
      document.getElementById("sign_rep"+id).className = "far fa-flag";
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
