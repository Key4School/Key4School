var min=0;
var sec=0;
var tmp="";

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
  $('#searchUser').keyup(function() {
    searchUser();
  });

  //scroll
  scroll();
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

  //scroll
  setTimeout(() => scroll(), 1000);
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
      if (html!=''){
        $('#messages').append(html); // on veut ajouter les nouveaux messages au début du bloc #messages
        scroll();
      }
    }
  });
}

setInterval(refresh, 1000);

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

}

function enleverRep() {
  document.getElementById('champReponse').innerHTML = "";
  document.getElementById('reponse').value = "None";
  document.getElementById('buttonRep').style.display = "none";
  document.getElementById('divrepmsg').style.backgroundColor = "";
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
          sec=0;
          min=0;
          mediaRecorder = new MediaRecorder(stream);
          mediaRecorder.start();
          stopped = false;
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
            form.append('group', idGroupe)
            estEnregistre = true;
            boutonAudioOpen();
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
          mediaRecorder = new MediaRecorder(stream);
          mediaRecorder.start();
          stopped = false;
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
            form.append('group', idGroupe)
            estEnregistre = true;
            boutonAudioOpen();
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
    $.ajax({
      url: "/uploadAudio/",
      type: "POST",
      data: form,
      processData: false,
      contentType: false,
      cache: false,
      success: function() {
        form = new FormData();
        estEnregistre = false;
        boutonAudioClose();
        document.getElementById('txtAudio').innerHTML = "";
      }
    });

    //scroll
    setTimeout(() => scroll(), 1000);
  }
}

function deleteAudio() {
  form = new FormData();
  estEnregistre = false;
  boutonAudioClose();
  document.getElementById('txtAudio').innerHTML = "";
}

function boutonAudioOpen() {
  document.getElementById('buttonAudio1').style.display = "block";
  document.getElementById('buttonAudio2').style.display = "block";
}

function boutonAudioClose() {
  document.getElementById('buttonAudio1').style.display = "none";
  document.getElementById('buttonAudio2').style.display = "none";
}
