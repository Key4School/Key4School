$(document).ready(function() {

  if (document.documentElement.getAttribute("data-theme") == "dark") {
    $(".sun").addClass("sun-logo");
    $(".moon").addClass("moon-logo");
  }
  if (document.documentElement.getAttribute("data-theme") == "light") {
    $(".sun").addClass("animate-sun");
    $(".moon").addClass("animate-moon");
  }
  if (document.documentElement.getAttribute("data-theme") == "system") {
    $("#systemTheme").prop('checked', true);
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      $(".sun").addClass("sun-logo");
      $(".moon").addClass("moon-logo");
      $(".sun").removeClass("animate-sun");
      $(".moon").removeClass("animate-moon");
    } else {
      $(".sun").removeClass("sun-logo");
      $(".moon").removeClass("moon-logo");
      $(".sun").addClass("animate-sun");
      $(".moon").addClass("animate-moon");
    }
  }
});

function themeRequest(theme){
  $.ajax({
    url: '/theme/', // on donne l'URL du fichier de traitement
    timeout: 5000,
    type: "POST", // la requête est de type POST
    data: {"theme": theme}, // et on envoie nos données
    error: function(xhr, textStatus, errorThrown) {
      location.reload();
    }
  });
}

function themefct() {
  document.querySelector(".sun").classList.toggle("animate-sun");
  document.querySelector(".moon").classList.toggle("animate-moon");
  document.querySelector(".sun").classList.toggle("sun-logo");
  document.querySelector(".moon").classList.toggle("moon-logo");
  $("#systemTheme").prop('checked', false);
  if (document.documentElement.getAttribute("data-theme") == "light") {
    localStorage.setItem('theme', 'dark');
    document.documentElement.setAttribute('data-theme', 'dark');
    themeRequest('dark');
  } else {
    localStorage.setItem('theme', 'light');
    document.documentElement.setAttribute('data-theme', 'light');
    themeRequest('light');
  }
}

function themeSysteme() {
  localStorage.setItem('theme', 'system');
  document.documentElement.setAttribute('data-theme', 'system');
  themeRequest('system');
  if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
    $(".sun").addClass("sun-logo");
    $(".moon").addClass("moon-logo");
    $(".sun").removeClass("animate-sun");
    $(".moon").removeClass("animate-moon");
  } else {
    $(".sun").removeClass("sun-logo");
    $(".moon").removeClass("moon-logo");
    $(".sun").addClass("animate-sun");
    $(".moon").addClass("animate-moon");
  }
}
function inputNom(){
  var contenu = $('#nom').html().trim();
  $('#nom').replaceWith('<div style="width:95%;width: calc(100% - 35px); margin-right: 15px; cursor: pointer;" class="input_inscription control has-icons-left has-icons-right"><input autocomplete="off" class="color_input input" placeholder="Nom" name="nom" id="nom" value="'+ contenu +'"><span class="icon is-small is-left"><i class="fas fa-user-alt"></i></span><span class="icon is-small is-right"><i class="fas fa-check" id="familyName_check"></i></span></div>'); // remplace le code HTML actuel par celui-ci
  $('#nom').keyup(function() {
    verifNom() ;
  });
}
function verifNom() {
  var $nom = $('#nom'),
      $familyName_check = $('#familyName_check');
  if ($nom.val().length < 3) { // si la chaîne de caractères est inférieure à 5
    $nom.css({ // on rend le champ rouge
      border: '3px solid red',
    });
    $familyName_check.removeClass("fas fa-check");
    $familyName_check.addClass("fas fa-times");
    $familyName_check.css({ // on rend le champ rouge
      color: 'red',
    });
    return false;
  } else {
    $nom.css({ // si tout est bon, on le rend vert
      border: '3px solid green',
    });
    $familyName_check.removeClass("fas fa-times");
    $familyName_check.addClass("fas fa-check");
    $familyName_check.css({ // on rend le champ rouge
      color: 'green',
    });
    return true;
  }
}
function inputPrenom(){
  var contenu = $('#prenom').html().trim();
  $('#prenom').replaceWith('<div style="width:95%;width: calc(100% - 35px); margin-right: 15px; cursor: pointer;" class="input_inscription control has-icons-left has-icons-right"><input class="color_input input" placeholder="Prénom" name="prenom" id="prenom" value="'+contenu+'"><span class="icon is-small is-left"><i class="fas fa-user-alt"></i></span><span class="icon is-small is-right"><i class="fas fa-check" id="name_check"></i></span></div>'); // remplace le code HTML actuel par celui-ci
  $('#prenom').keyup(function() {
    verifPrenom() ;
  });
}
function verifPrenom() {
  var $prenom = $('#prenom'),
      $name_check = $('#name_check');
  if ($prenom.val().length < 2) { // si la chaîne de caractères est inférieure à 5
    $prenom.css({ // on rend le champ rouge
      border: '3px solid red',
    });
    $name_check.removeClass("fas fa-check");
    $name_check.addClass("fas fa-times");
    $name_check.css({ // on rend le champ rouge
      color: 'red',
    });
    return false;
  } else {
    $prenom.css({ // si tout est bon, on le rend vert
      border: '3px solid green',
    });
    $name_check.removeClass("fas fa-times");
    $name_check.addClass("fas fa-check");
    $name_check.css({ // on rend le champ rouge
      color: 'green',
    });
    return true;
  }
}
function inputPseudo(){
  var contenu = $('#pseudo').html().trim();
  $('#pseudo').replaceWith('<div style="width:95%;width: calc(100% - 35px); margin-right: 15px; cursor: pointer;" class="input_inscription control has-icons-left has-icons-right"><input autocomplete="off" class="color_input input" type="text" placeholder="Pseudo" name="pseudo" id="pseudo" value="' + contenu +'"><span class="icon is-small is-left"><i class="far fa-smile-wink"></i></span><span class="icon is-small is-right"><i class="fas fa-check" id="pseudo_check"></i></span></div>'); // remplace le code HTML actuel par celui-ci
  $('#pseudo').keyup(function() {
    verifPseudo() ;
  });
}
function verifPseudo() {
  var $pseudo = $('#pseudo'),
      $pseudo_check = $('#pseudo_check');
  if ($pseudo.val().length < 4) { // si la chaîne de caractères est inférieure à 5
    $pseudo.css({ // on rend le champ rouge
      border: '3px solid red',
    });
    $pseudo_check.removeClass("fas fa-check");
    $pseudo_check.addClass("fas fa-times");
    $pseudo_check.css({ // on rend le champ rouge
      color: 'red',
    });
    return false;
  } else {
    $pseudo.css({ // si tout est bon, on le rend vert
      border: '3px solid green',
    });
    $pseudo_check.removeClass("fas fa-times");
    $pseudo_check.addClass("fas fa-check");
    $pseudo_check.css({ // on rend le champ rouge
      color: 'green',
    });
    return true;
  }
}

function inputLycee(){
  var contenu = $('#lycee').html().trim();
  $('#lycee').replaceWith('<div style="width:95%;width: calc(100% - 35px); margin-right: 15px; cursor: pointer;" class="input_inscription control has-icons-left has-icons-right"><input autocomplete="off" class="color_input input" type="text" placeholder="Lycée" id="school" value="' + contenu +'"><span class="icon is-small is-left"><i class="fas fa-school"></i></span><span class="icon is-small is-right"><i class="fas fa-check" id="school_check"></i></span></div><input type="hidden" name="school" id="schoolValue">'); // remplace le code HTML actuel par celui-ci
  $('#school').on('change keyup focus', function() {
    verifSchool(true);
  });
}

function verifSchool(asynch) {
  var $school = $('#school'),
      $school_check = $('#school_check');
  var retour;
  $.ajax({
    url: 'https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-en-annuaire-education&facet=nom_etablissement&facet=nom_commune&refine.type_etablissement=Lycée',
    dataType: 'json',
    async: asynch,
    data: {
      q: $('#school').val()
    },
    success: function(donnee) {
      lycee = [];
      lyceesValues = {};
      $.map(donnee, function() {
        for (let i = 0; i < donnee["records"].length; i++) {
          if (lycee.length <= 10) {
            var nomVille = donnee["records"][i]["fields"]["nom_etablissement"] + ' ' + donnee["records"][i]["fields"]["nom_commune"];
            var lyceeVal = JSON.stringify({'nomVille': nomVille, 'id': donnee["records"][i]["fields"]["identifiant_de_l_etablissement"]});
            if (lycee.indexOf(nomVille) === -1) {
              lycee.push(nomVille);
              lyceesValues[nomVille] = lyceeVal;
            }
          }
        }
      });

      $('#school').autocomplete({
        autoFocus: true,
        source: lycee,
        minLength:0
      });

      if (lycee.indexOf($school.val()) === -1) {
        $school.css({ // on rend le champ rouge
          border: '3px solid red',
        });
        $school_check.removeClass("fas fa-check");
        $school_check.addClass("fas fa-times");
        $school_check.css({ // on rend le champ rouge
          color: 'red',
        });
        retour = false;
      } else {
        $school.css({ // si tout est bon, on le rend vert
          border: '3px solid green',
        });
        $school_check.removeClass("fas fa-times");
        $school_check.addClass("fas fa-check");
        $school_check.css({ // on rend le champ rouge
          color: 'green',
        });
        $('#schoolValue').val(lyceesValues[$school.val()]);
        retour = true;
      }
    }
  });
  return retour;
}
$form.on('submit', function() {
  if (verifNom() && verifPrenom() && verifPseudo() && verifSchool(false)) {
    return true;
  } else {
    return false;
  }
});


function updateImgOpen() {
  $("#replaceImg").addClass("is-active");
}

function updateImgClose() {
  $("#replaceImg").removeClass("is-active");
}

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
