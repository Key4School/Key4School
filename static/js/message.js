var min=0;
var sec=0;
var tmp="";
var idMsg;

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
  /*searchUser();
  $('#searchUser').keyup(function() {
    searchUser();
  });*/

  //scroll
  scroll();
  $('#inputMsg').focus();
});

const scroll = () => {
  const messagesDiv = document.getElementById('messages');
  const scrollHeight = messagesDiv.scrollHeight;

  return messagesDiv.scrollBy(0, scrollHeight);
};

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
  const contenuMsg = document.getElementById('inputMsg').value || '';
  const reponse = document.getElementById('reponse').value || '';

  socket.emit('postMsg', {room: idGroupe, contenuMessage: contenuMsg, reponse: reponse});

  $('#messageForm').trigger("reset");
  enleverRep();
  scroll();
}

/*function searchUser() {
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
}*/

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

const messages = document.getElementById('messages');

var start = new Date();

const socket = io(`ws://${document.location.host}`);
const idGroupe = document.getElementById('idGroupe').value || undefined;

socket.on('connect', function() {
  if (idGroupe != "None"){
    socket.emit('connectToGroup', {room: idGroupe});
  }
});

socket.on('newMsg', (html) => {
  var scrollHeight = $('#messages')[0].scrollHeight - $('#messages')[0].offsetHeight;
  $('#messages').append(html); // on veut ajouter les nouveaux messages au début du bloc #messages
  if ($('#messages').scrollTop() >= scrollHeight){
    scroll();
  }
});


function reponseMsg(nb) {
  var contentMsg = document.getElementById('contenu' + nb).value;
  var pseudo = document.getElementById('user' + nb).value;
  repmsg = document.getElementById('messageForm');
  document.getElementById('divrepmsg').style.backgroundColor = "rgb(218 255 250)";
  document.getElementById('champReponse').innerHTML =
  "<div style='background-color:rgb(198 235 231 / 1);padding:1%;padding-left:2%;border-left:4px solid blue;border-radius:7px;'>"
   + pseudo +
   '<br>' +
   contentMsg +
   "</div>";
  document.getElementById('reponse').value = nb;
  idMsg = "None";
  contentMsg = "";
  document.getElementById('buttonRep').style.display = "block";
  $('#inputMsg').focus();
}

function enleverRep() {
  document.getElementById('champReponse').innerHTML = "";
  document.getElementById('reponse').value = "None";
  document.getElementById('buttonRep').style.display = "none";
  document.getElementById('divrepmsg').style.backgroundColor = "";
  $('#inputMsg').focus();
}


let shouldStop = false;
let stopped = true;
const audioMsg = document.getElementById('audioMsg');
const stopButton = document.getElementById('stop');
var mediaRecorder = "";
var form = new FormData();
var accessMicro = false;
var estEnregistre = "";

function micro() {
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({
      audio: true
    });
    accessMicro = true;
  }
}

function enregistrer(e) {
  var touche = event.keyCode;
  console.log(touche);
  if (touche == 80 && stopped == true) {
    if (accessMicro == true) {
      navigator.mediaDevices.getUserMedia(
          // constraints - only audio needed for this app
          {
            audio: true
          })

        // Success callback
        .then(function(stream) {
          boutonAudioOpen();
          sec=0;
          min=0;
          mediaRecorder = new MediaRecorder(stream);
          mediaRecorder.start();
          stopped = false;
          sec = 0;
          min =0;
          document.getElementById('txtAudio').innerHTML = "0:0";
          chrono = setInterval(function(){
            sec+=1
            if (sec>=60){
              sec=0
              min+=1
            }
          tmp= min + ":" + sec
          document.getElementById('txtAudio').innerHTML = tmp;
          }, 1000);
          console.log(mediaRecorder.state);
          console.log("recorder started");
          let chunks = [];
          mediaRecorder.ondataavailable = function(e) {
            chunks.push(e.data);
          }
          mediaRecorder.onstop = function(e) {
            console.log(chunks);
            const blob = new Blob(chunks, {
              'type': 'audio/ogg; codecs=opus'
            });
            chunks = [];
            console.log(blob);
            var idGroupe = $('[name="group"]').attr("value");
            form.append('audio', blob);
            estEnregistre = true;
            document.getElementById('txtAudio').innerHTML = tmp;
            clearTimeout(chrono);
          }
        })

        // Error callback
        .catch(function(err) {
          console.log('The following getUserMedia error occurred: ' + err);
        });
    } else {
      micro();
    }
  }
}





function stop(e) {
  var touche = event.keyCode;
  if (touche == 80) {
    if (stopped == false) {
      mediaRecorder.stop();
      console.log(mediaRecorder.state);
      console.log("recorder stopped");
      stopped = true;
    }
  }
}

function enregistrerTel() {
  if (stopped == true) {
    if (accessMicro == true) {
      navigator.mediaDevices.getUserMedia(
          // constraints - only audio needed for this app
          {
            audio: true
          })

        // Success callback
        .then(function(stream) {
          boutonAudioOpen();
          mediaRecorder = new MediaRecorder(stream);
          mediaRecorder.start();
          stopped = false;
          sec = 0;
          min =0;
          document.getElementById('txtAudio').innerHTML = "0:0";
          chrono = setInterval(function(){
            sec+=1
            if (sec>=60){
              sec=0
              min+=1
            }
          tmp= min + ":" + sec
          document.getElementById('txtAudio').innerHTML = tmp;
          }, 1000);
          console.log(mediaRecorder.state);
          console.log("recorder started");
          let chunks = [];
          mediaRecorder.ondataavailable = function(e) {
            console.log('ok');
            chunks.push(e.data);
          }
          mediaRecorder.onstop = function(e) {
            console.log(chunks);
            const blob = new Blob(chunks, {
              'type': 'audio/ogg; codecs=opus'
            });
            chunks = [];
            console.log(blob);
            var idGroupe = $('[name="group"]').attr("value");
            form.append('audio', blob);
            estEnregistre = true;
            clearTimeout(chrono);
          }
        })

        // Error callback
        .catch(function(err) {
          console.log('The following getUserMedia error occurred: ' + err);
        });
    } else {
      micro();
    }
  }
}

function stopTel() {
  if (stopped == false) {
    mediaRecorder.stop();
    console.log(mediaRecorder.state);
    console.log("recorder stopped");
    stopped = true;
  }
}

function sendAudio() {
  if (estEnregistre = true) {
    var datetime = new Date().toISOString().replace(/Z/, '+00:00');
    form.append('date', datetime);
    form.append('group', idGroupe);
    $.ajax({
      url: "/uploadAudio/",
      type: "POST",
      data: form,
      processData: false,
      contentType: false,
      cache: false,
      success: function() {
        socket.emit('postMsg', {room: idGroupe, reponse: 'None', dateAudio: datetime});
        form = new FormData();
        estEnregistre = false;
        boutonAudioClose();
        document.getElementById('txtAudio').innerHTML = "";
        scroll();
      }
    });
  }
}

function deleteAudio() {
  form = new FormData();
  estEnregistre = false;
  while (document.getElementById('txtAudio').innerHTML != ""){
    document.getElementById('txtAudio').innerHTML = "";
  }
  boutonAudioClose();
}

function boutonAudioOpen() {
  document.getElementById('buttonAudio1').style.display = "block";
  document.getElementById('buttonAudio2').style.display = "block";
}

function boutonAudioClose() {
  document.getElementById('buttonAudio1').style.display = "none";
  document.getElementById('buttonAudio2').style.display = "none";
  while (document.getElementById('txtAudio').innerHTML != ""){
    document.getElementById('txtAudio').innerHTML = "";
  }
}

function signalisationDiscussion() {
  selectionSign = document.getElementById("sign").className
  if (selectionSign == "far fa-flag") {
    signalisationDiscussionOpen();


  }
  if (selectionSign == "fas fa-flag"){
    designalisationDiscussionOpen();
  }
}

function signalisationDiscussionClose(){
  $("#signalisationDiscussion").removeClass("is-active");
}

function signalisationDiscussionOpen(){
  $("#signalisationDiscussion").addClass("is-active");
}

function designalisationDiscussionClose(){
  $("#designalisationDiscussion").removeClass("is-active");
}

function designalisationDiscussionOpen(){
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
function signalisationMsg (idMsg) {
  selectionSignMsg = document.getElementById("signMsg_"+idMsg).className
  if (selectionSignMsg == "far fa-flag") {
    document.getElementById("idMsgSignalé").value = idMsg;
    signalisationMsgOpen();
  }
  if (selectionSignMsg == "fas fa-flag"){
    document.getElementById("idMsgDeSignalé").value = idMsg;
    designalisationMsgOpen();
  }
}

function signalisationMsgClose(){
  $("#signalisationMsg").removeClass("is-active");
}

function signalisationMsgOpen(){
  $("#signalisationMsg").addClass("is-active");
}

function designalisationMsgClose(){
  $("#designalisationMsg").removeClass("is-active");
}

function designalisationMsgOpen(){
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
      idMsg=document.getElementById('idMsgSignalé').value;
      document.getElementById("signMsg_"+idMsg).className = "fas fa-flag";
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
      idMsg=document.getElementById('idMsgDeSignalé').value;
      document.getElementById("signMsg_"+idMsg).className = "far fa-flag";
      document.getElementById("sign").className = "far fa-flag";
      designalisationMsgClose();
    },
  });
}
