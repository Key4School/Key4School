var min = 0;
var sec = 0;
var tmp = "";
var idMsg;

$(document).ready(function() {
  $('#titreetmsg').css({
    height: ($(window).height() - parseInt(window.getComputedStyle(document.getElementById('nav'), null).getPropertyValue('height').replace(/px/, '')) - 90).toString() + 'px',
    //width: (80 / 100 * ($(window).width())).toString() + 'px',
  });
  $('#divCoteMessage').css({
    height: ($(window).height() - parseInt(window.getComputedStyle(document.getElementById('nav'), null).getPropertyValue('height').replace(/px/, '')) - 120).toString() + 'px',
    //width: (80 / 100 * ($(window).width())).toString() + 'px',
  });

  $('#nomgroupe').css({
    height: ($(window).height() - parseInt(window.getComputedStyle(document.getElementById('nav'), null).getPropertyValue('height').replace(/px/, '')) - 40).toString() + 'px',
  });
  $('#listeuser').css({
    height: (40 / 100 * ($(window).height())).toString() + 'px',
  });
  $('#content_input_nom_groupe').css({
    display: "none",
  });
  /*searchUser();
  $('#searchUser').keyup(function() {
    searchUser();
  });*/
  // Affichage nb de participants, en fonction de la taille de l'écran
  const groupTitle_size = parseInt(window.getComputedStyle(document.getElementById('groupTitle'), null).getPropertyValue('height').replace(/px/, ''));
  let listGroupUsers_size = parseInt(window.getComputedStyle(document.getElementById('listGroupUsers'), null).getPropertyValue('height').replace(/px/, ''));
  if (groupTitle_size + listGroupUsers_size > 88) {
    document.getElementById('listGroupUsers').innerHTML += `<br />&nbsp;<a style="margin-left: 15px;" onclick="divoptionopen()"><em>et <span id="lastedGroupUsers">0</span> autres utilisateurs</em></a>`;
    const lastedGroupUsers_count = document.getElementById('lastedGroupUsers');

    while (groupTitle_size + listGroupUsers_size > 88) {
      listGroupUsers_size = parseInt(window.getComputedStyle(document.getElementById('listGroupUsers'), null).getPropertyValue('height').replace(/px/, ''));
      showedGroupUsers = document.querySelectorAll('.groupUser[style="display: inline;"]');
      // hide last user
      showedGroupUsers[showedGroupUsers.length - 1].style.display = 'none';
      // add count of lasted users
      lastedGroupUsers_count.innerHTML = parseInt(lastedGroupUsers_count.innerHTML) + 1;
    }
  }

  //scroll
  scroll();
  $('#inputMsg').focus();
});

const scroll = () => {
  const messagesDiv = document.getElementById('messages');
  if (messagesDiv !== null) {
    const scrollHeight = messagesDiv.scrollHeight;

    return messagesDiv.scrollBy(0, scrollHeight);
  }
};



function checkboxTitle() {
  var inputElems = document.getElementsByTagName("input"),
    count = 0;
  for (var i = 0; i < inputElems.length; i++) {
    if (inputElems[i].type === "checkbox" && inputElems[i].checked === true) {
      count++;
      if (count > 1) {
        $('#content_input_nom_groupe').css({
          display: "block"
        });
        $("[name='nomnewgroupe']").attr("required", true);
        $('#switchGroupeMP').css({
          display: "none"
        });
      }
      if (count == 1) {
        $('#content_input_nom_groupe').css({
          display: "none"
        });
        $("[name='nomnewgroupe']").attr("required", false);
        $('#switchGroupeMP').css({
          display: "block"
        });
      }
    }
  }
}

$('#checkGroupeMP').change(function() {
  if ($('#checkGroupeMP').hasClass("checked") == true) {
    $('#content_input_nom_groupe').css({
      display: "none"
    });
    $("[name='nomnewgroupe']").attr("required", false);
    $('#checkGroupeMP').removeClass("checked");
  }
  else {
    $('#checkGroupeMP').addClass("checked");
    $('#content_input_nom_groupe').css({
      display: "block"
    });
    $("[name='nomnewgroupe']").attr("required", true);
  }
});

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
  if (document.getElementById('inputImage').files.length > 0) {
    sendImage();
    return;
  }

  const contenuMsg = document.getElementById('inputMsg').value || '';
  const reponse = document.getElementById('reponse').value || 'None';

  if (contenuMsg !== '')
    socket.emit('postMsg', { room: idGroupe, contenuMessage: contenuMsg, reponse: reponse });

  $('#messageForm').trigger("reset");
  enleverRep();
  resetImage();
  scroll();
}

// $('#messages').ondragover = $('#messages').ondragenter = function(evt) {
//   evt.preventDefault();
// };
//
// $('#messages').ondrop = function(evt) {
//   // pretty simple -- but not for IE :(
//   $('#inputImage').files = evt.dataTransfer.files;
//
//   // If you want to use some of the dropped files
//   const dT = new DataTransfer();
//   dT.items.add(evt.dataTransfer.files[0]);
//   dT.items.add(evt.dataTransfer.files[3]);
//   $('#inputImage').files = dT.files;
//
//   evt.preventDefault();
// };


var $dropzone = document.querySelector('#titreetmsg');

$dropzone.ondragover = function(e) {
  e.preventDefault();
  $('#messages').addClass('dragover');
  $('#divDansTitregroupe').addClass('dragover');
};
$dropzone.ondragleave = function(e) {
  e.preventDefault();
  $('#messages').removeClass('dragover');
  $('#divDansTitregroupe').removeClass('dragover');
  resetImage();
};
$dropzone.ondrop = function(e) {
  e.preventDefault();
  $('#messages').removeClass('dragover');
  $('#divDansTitregroupe').removeClass('dragover');
  document.getElementById('inputImage').files = e.dataTransfer.files;
  var fichier = e.dataTransfer.files;
  var reader = new FileReader();
  reader.onload = function(event) {
    // $('#image').attr('src', event.target.result);
    $("#divImgTmp").append('<img alt="image messages" src="' + event.target.result + '"style="height: auto;max-height:80%;max-width:80%;bottom: 0;right: calc(50% - 100px);" id="image" />');
  }
  reader.readAsDataURL(fichier[0]);
  imageUploaded();
}

function imageUploaded() {
  $('#inputImage').css('display', 'none');
  $('#uploadImageIcon').css('display', 'none');
  $('#resetImageIcon1').css('display', 'inline-block');
  $('#resetImageIcon2').css('display', 'inline-block');
  $('#messages').css('display', 'none');
  $('#divImgTmp').css('display', 'block');
}

function suppTmpMsg() {
  // $("#image").attr("src", "");
  $("#image").remove();
  $('#messages').css('display', 'flex');
  $('#divImgTmp').css('display', 'none');
}

function resetImage() {
  $('#inputImage').val('');
  $('#inputImage').css('display', 'block');
  $('#uploadImageIcon').css('display', 'inline-block');
  $('#resetImageIcon1').css('display', 'none');
  $('#resetImageIcon2').css('display', 'none');
  suppTmpMsg()
}

function sendImage() {
  var formImage = new FormData(document.getElementById('messageForm'));
  $.ajax({
    url: "/uploadImage/",
    type: "POST",
    data: formImage,
    processData: false,
    contentType: false,
    cache: false,
    success: function() {
      $('#messageForm').trigger("reset");
      enleverRep();
      resetImage();
      scroll();
    }
  });
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

const idGroupe = document.getElementById('idGroupe').value || undefined;
const idUser = document.getElementById('idUser').value || undefined;

socket.on('connect', function() {
  if (idGroupe != "None") {
    socket.emit('connectToGroup', { room: idGroupe });
  }
});

socket.on('newMsg', (data) => {
  var scrollHeight = $('#messages')[0].scrollHeight - $('#messages')[0].offsetHeight;

  if (data.fromUser == idUser)
    $('#messages').append(data.ownHTML); // on veut ajouter les nouveaux messages au début du bloc #messages
  else
    $('#messages').append(data.otherHTML); // on veut ajouter les nouveaux messages au début du bloc #messages

  if ($('#messages').scrollTop() >= scrollHeight) {
    scroll();
  }
});

$(window).data('ajaxready', true);

// load 40 messages at loading
for (let i = 0; i < 2; i++) {
  $.ajax({
    url: "/moreMsg/", // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: {
      'lastMsg': $('#messages > div').length,
      'idGroupe': idGroupe
    }, // et on envoie nos données
    success: function(json) {
      if (json.html != '') {
        $('#messages').prepend(json.html);
      }
      scroll();
    }
  });
}

var lastScrollTop = $('#messages').scrollTop();

$('#messages').scroll(() => {
  if ($(window).data('ajaxready') == false) return;

  var scrollHeight = $('#messages')[0].scrollHeight - $('#messages')[0].offsetHeight;
  var scrollTop = $('#messages').scrollTop();

  if (scrollTop <= lastScrollTop) {
    $(window).data('ajaxready', false);
    $.ajax({
      url: "/moreMsg/", // on donne l'URL du fichier de traitement
      type: "POST", // la requête est de type POST
      data: {
        'lastMsg': $('#messages > div').length,
        'idGroupe': idGroupe
      }, // et on envoie nos données
      success: function(json) {
        if (json.html != '') {
          $('#messages').prepend(json.html);
          $(window).data('ajaxready', true);
        }
      }
    });
  }
  lastScrollTop = scrollTop;
});

function reponseMsg(nb) {
  document.getElementById('divrepmsg').style.display = "flex";
  var contentMsg = document.getElementById('contenu' + nb).value;
  console.log(contentMsg);
  var pseudo = document.getElementById('user' + nb).value;
  repmsg = document.getElementById('messageForm');
  document.getElementById('divrepmsg').style.backgroundColor = couleur_deux;
  //document.getElementById('messages').style.height = "65%";
  document.getElementById('champReponse').innerHTML =
    "<div style='background-color:" + couleur_deux + ";padding:0.5%;padding-left:2%;border-left:4px solid " + couleur_un + ";border-radius:7px;'>"
    + pseudo +
    '<br>' +
    contentMsg +
    "</div>";
  document.getElementById('reponse').value = nb;
  idMsg = "None";
  contentMsg = "";
  document.getElementById('buttonRep').style.display = "block";
  document.getElementById('divrepmsg').style.top = `calc(100% - ${(parseInt(window.getComputedStyle(document.getElementById('nav'), null).getPropertyValue('height').replace(/px/, '')) + 20).toString() + 'px'})`;
  $('#inputMsg').focus();
}

function enleverRep() {
  document.getElementById('divrepmsg').style.display = "none";
  //document.getElementById('messages').style.height = "80%";
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
var final;
var options = {
  audioBitsPerSecond: 56000
}

function micro() {
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({
      audio: true
    });
    accessMicro = true;
    enregistrerTel();
  }
}

// function enregistrer(e) {
//   var touche = event.keyCode;
//   console.log(touche);
//   if (touche == 80 && stopped == true) {
//     if (accessMicro == true) {
//       navigator.mediaDevices.getUserMedia(
//           // constraints - only audio needed for this app
//           {
//             audio: true
//           })
//
//         // Success callback
//         .then(function(stream) {
//           boutonAudioOpen();
//           sec=0;
//           min=0;
//           mediaRecorder = new MediaRecorder(stream);
//           mediaRecorder.start();
//           stopped = false;
//           sec = 0;
//           min =0;
//           document.getElementById('txtAudio').innerHTML = "0:0";
//           chrono = setInterval(function(){
//             sec+=1
//             if (sec>=60){
//               sec=0
//               min+=1
//             }
//           tmp= min + ":" + sec
//           document.getElementById('txtAudio').innerHTML = tmp;
//           }, 1000);
//           console.log(mediaRecorder.state);
//           console.log("recorder started");
//           let chunks = [];
//           mediaRecorder.ondataavailable = function(e) {
//             chunks.push(e.data);
//           }
//           mediaRecorder.onstop = function(e) {
//             console.log(chunks);
//             const blob = new Blob(chunks, {
//               'type': 'audio/ogg; codecs=opus'
//             });
//             chunks = [];
//             console.log(blob);
//             var idGroupe = $('[name="group"]').attr("value");
//             form.append('audio', blob);
//             estEnregistre = true;
//             document.getElementById('txtAudio').innerHTML = tmp;
//             clearTimeout(chrono);
//           }
//         })
//
//         // Error callback
//         .catch(function(err) {
//           console.log('The following getUserMedia error occurred: ' + err);
//         });
//     } else {
//       micro();
//     }
//   }
// }
//
//
//
//
//
// function stop(e) {
//   var touche = event.keyCode;
//   if (touche == 80) {
//     if (stopped == false) {
//       mediaRecorder.stop();
//       console.log(mediaRecorder.state);
//       console.log("recorder stopped");
//       stopped = true;
//     }
//   }
// }

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
          mediaRecorder = new MediaRecorder(stream, options);
          mediaRecorder.start();
          stopped = false;
          sec = 0;
          min = 0;
          document.getElementById('txtAudio').innerHTML = "0:0";
          chrono = setInterval(function() {
            sec += 1
            if (sec >= 60) {
              sec = 0
              min += 1
            }
            tmp = min + ":" + sec
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
            if (final == "jeter") {
              deleteAudio();
            } else if (final == "garder") {
              sendAudio();
            }
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

function stopTel(but) {
  final = but;
  if (stopped == false) {
    mediaRecorder.stop();
    console.log(mediaRecorder.state);
    console.log("recorder stopped");
    stopped = true;
  }
}

function sendAudio() {
  if (estEnregistre = true) {
    const reponse = document.getElementById('reponse').value || 'None';
    form.append('group', idGroupe);
    form.append('reponse', reponse);
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
        enleverRep();
        document.getElementById('txtAudio').innerHTML = "";
        scroll();
      }
    });
  }
}

function deleteAudio() {
  form = new FormData();
  estEnregistre = false;
  while (document.getElementById('txtAudio').innerHTML != "") {
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
  while (document.getElementById('txtAudio').innerHTML != "") {
    document.getElementById('txtAudio').innerHTML = "";
  }
}

function changeRate(id) {
  myaudio = document.getElementById("audio" + id);
  if (myaudio.playbackRate == 2) {
    myaudio.playbackRate = 1;
    document.getElementById("buttonAudio" + id).innerHTML = "1x";
  } else if (myaudio.playbackRate == 1) {
    myaudio.playbackRate = 1.5;
    document.getElementById("buttonAudio" + id).innerHTML = "1.5x";
  } else if (myaudio.playbackRate == 1.5) {
    myaudio.playbackRate = 2;
    document.getElementById("buttonAudio" + id).innerHTML = "2x";
  }
}




// const playIconContainer = document.getElementById('play-icon');
// const audioPlayerContainer = document.getElementById('audio-player-container');
// const seekSlider = document.getElementById('seek-slider');
// const audio = document.querySelector('audio');
// let playState = 'pause';
//
// playIconContainer.removeAttribute('onclick');
//
//
// playIconContainer.addEventListener('click', () => {
//     if(playState === 'play') {
//         audio.pause();
//         cancelAnimationFrame(raf);
//         playState = 'pause';
//         playIconContainer.innerHTML = "play";
//     } else {
//         audio.play();
//         requestAnimationFrame(whilePlaying);
//         playState = 'play';
//         playIconContainer.innerHTML = "pause";
//     }
// });
//
//
//
// const showRangeProgress = (rangeInput) => {
//     if(rangeInput === seekSlider) audioPlayerContainer.style.setProperty('--seek-before-width', rangeInput.value / rangeInput.max * 100 + '%');
// }
//
// seekSlider.addEventListener('input', (e) => {
//     showRangeProgress(e.target);
// });
//
// const durationContainer = document.getElementById('duration');
// const currentTimeContainer = document.getElementById('current-time');
// let raf = null;
//
// const calculateTime = (secs) => {
//     const minutes = Math.floor(secs / 60);
//     const seconds = Math.floor(secs % 60);
//     const returnedSeconds = seconds < 10 ? `0${seconds}` : `${seconds}`;
//     return `${minutes}:${returnedSeconds}`;
// }
//
// const displayDuration = () => {
//     durationContainer.textContent = calculateTime(audio.duration);
// }
//
// const setSliderMax = () => {
//     seekSlider.max = Math.floor(audio.duration);
// }
//
// const displayBufferedAmount = () => {
//     const bufferedAmount = Math.floor(audio.buffered.end(audio.buffered.length - 1));
//     audioPlayerContainer.style.setProperty('--buffered-width', `${(bufferedAmount / seekSlider.max) * 100}%`);
// }
//
// const whilePlaying = () => {
//     seekSlider.value = Math.floor(audio.currentTime);
//     currentTimeContainer.textContent = calculateTime(seekSlider.value);
//     audioPlayerContainer.style.setProperty('--seek-before-width', `${seekSlider.value / seekSlider.max * 100}%`);
//     raf = requestAnimationFrame(whilePlaying);
// }
//
// if (audio.readyState > 0) {
//     displayDuration();
//     setSliderMax();
//     displayBufferedAmount();
// } else {
//     audio.addEventListener('loadedmetadata', () => {
//         displayDuration();
//         setSliderMax();
//         displayBufferedAmount();
//     });
// }
//
// audio.addEventListener('progress', displayBufferedAmount);
//
// seekSlider.addEventListener('input', () => {
//     currentTimeContainer.textContent = calculateTime(seekSlider.value);
//     if(!audio.paused) {
//         cancelAnimationFrame(raf);
//     }
// });
//
// seekSlider.addEventListener('change', () => {
//     audio.currentTime = seekSlider.value;
//     if(!audio.paused) {
//         requestAnimationFrame(whilePlaying);
//     }
// });
//
// audio.addEventListener("ended", function(){
//      audio.currentTime = 0;
//      playState = 'pause';
//      playIconContainer.innerHTML = "play";
// });
// }

function optionParticipantOpen(id) {
  $("#optionParticipant").addClass("is-active");
  document.getElementById("hrefParticipant").href = "/profil/" + id;
  document.getElementById("idViré2").value = id;
}

function optionParticipantClose() {
  $("#optionParticipant").removeClass("is-active");
}

function modifRole(id, idGrp) {
  $.ajax({
    url: '/modifRole/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: ({ idModifié: id, idGrp: idGrp }), // et on envoie nos données
    success: function(response) {
      if (response === 'participant') {
        document.getElementById("ModifRoleUser" + id).parentElement.innerHTML = '<span class="icon is-small">' +
          '<i class="fas fa-users" aria-hidden="true"></i>' +
          '</span>' +
          `<span id="ModifRoleUser${id}">Participant</span>`;
        document.getElementById("ModifRoleUser" + id).parentElement.classList.remove('is-warning');
        document.getElementById("ModifRoleUser" + id).parentElement.classList.add('is-info');
      }
      else if (response === 'admin') {
        document.getElementById("ModifRoleUser" + id).parentElement.innerHTML = '<span class="icon is-small">' +
          '<i class="fas fa-crown" aria-hidden="true"></i>' +
          '</span>' +
          `<span id="ModifRoleUser${id}">Admin</span>`;
        document.getElementById("ModifRoleUser" + id).parentElement.classList.remove('is-info');
        document.getElementById("ModifRoleUser" + id).parentElement.classList.add('is-warning');
      }
    },
  });
}

function ajouterParticipantVoir() {
  if (document.getElementById("ajouterParticipant").style.display == "none") {
    document.getElementById("ajouterParticipant").style.display = "block";
    document.getElementById("buttonAjouterParticipantOpen").style.display = "none";
    document.getElementById("buttonAjouterParticipantClose").style.display = "block";
  } else {
    document.getElementById("ajouterParticipant").style.display = "none";
    document.getElementById("buttonAjouterParticipantOpen").style.display = "block"
    document.getElementById("buttonAjouterParticipantClose").style.display = "none";

  }
}

function quitterGroupe(e) {
  e.preventDefault();
  var donnees = $('#quitterGroupeForm').serialize();
  $.ajax({
    url: '/virerParticipant/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      if (response == 'reload msg') {
        document.location.href = '/messages';
      } else {
        location.reload();
      }
    },
  });
}

function quitterGroupeOpen(grpID, userID, id) {
  $("#quitterGroupe").addClass("is-active");
  if (userID == id) {
    document.getElementById('pop up virer').innerHTML = "Etes-vous sûr de vouloir quitter le groupe ?";
  } else {
    document.getElementById('pop up virer').innerHTML = "Etes-vous sûr de vouloir enlever ce participant ?";
  }
}

function quitterGroupeClose() {
  $("#quitterGroupe").removeClass("is-active");
}

function supprimerGroupe(e) {
  const idGrp = document.getElementById('supprimerGroupeId').value;

  fetch(`/supprGroupe/${idGrp}/`, {
    method: 'post',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  })
    .then(res => document.location.href = '/messages/');
}

function supprimerGroupeOpen() {
  $("#supprimerGroupe").addClass("is-active");
}

function supprimerGroupeClose() {
  $("#supprimerGroupe").removeClass("is-active");
}

function updateGroupName() {
  const newGrpName = document.getElementById('newGrpName').value.trim();

  if (newGrpName !== '') {
    document.querySelector(`.listedGrp[data-grpid="${idGroupe}"] .grpName`).innerHTML = newGrpName;
    document.querySelector(`.listedGrp[data-grpid="${idGroupe}"]`).dataset.grpname = newGrpName;
    document.querySelector('#groupTitle > .grpName').innerHTML = newGrpName;

    fetch(`/updateGrpName/${idGroupe}/${newGrpName}/`, {
      method: 'post',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
    });

    divoptionclose();
  }
}

function modererGrp(idGrp) {
  const infoGrpModeration = document.getElementById('infoGrpModeration');

  if (infoGrpModeration.innerHTML === 'Groupe auto-modéré')
    infoGrpModeration.innerHTML = 'Groupe non auto-modéré';
  else
    infoGrpModeration.innerHTML = 'Groupe auto-modéré';

  fetch(`/modererGrp/${idGrp}/`, {
    method: 'post',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  });
}

const goToMess = async (idMsg) => {
  if (document.getElementById(idMsg) === null) {
    await $.ajax({
      url: "/moreMsg/", // on donne l'URL du fichier de traitement
      type: "POST", // la requête est de type POST
      data: {
        'lastMsg': $('#messages > div').length,
        'idGroupe': idGroupe
      }, // et on envoie nos données
      success: function(json) {
        if (json.html != '') {
          $('#messages').prepend(json.html);
        }
      }
    });
    return goToMess(idMsg);
  }

  // return window.location.hash = `#${idMsg}`;
  await document.getElementById(idMsg).scrollIntoView({ behavior: "smooth" });
  setTimeout(() => {
    document.getElementById(idMsg).scrollIntoView()
  }, 500);

  return;
};

document.getElementById("inputImage").onchange = function() {
  var reader = new FileReader();

  reader.onload = function(e) {
    // get loaded data and render thumbnail.
    // document.getElementById("image").src = e.target.result;
    $("#divImgTmp").append('<img alt="image messages" src="' + e.target.result + '"style="height: auto;max-height:80%;max-width:80%;bottom: 0;right: calc(50% - 100px);" id="image" />');
  };

  // read the image file as a data URL.
  reader.readAsDataURL(this.files[0]);
};
