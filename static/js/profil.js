var boul1 = false;
var boul2 = false;
var boul3 = false;
var boul4 = false;
$(document).ready(function() {
  $('#delete').click(function() {
    console.log('ok');
    $('.contenu').addClass("active"),
      $("#delete").css("zIndex", "-1");
    $("#ConfSupp-filtre").css("display", "block");
  });
  $('#updateProfil').on('submit', function() {
    alert(verifNom(), verifPrenom(), verifPseudo(), verifSchool(false), verifMdp(), verifConfMdp());
    if (verifNom() && verifPrenom() && verifPseudo() && verifSchool(false) && verifMdp() && verifConfMdp()) {
      return true;
    } else {
      return false;
    }
  });
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

function themeRequest(theme) {
  $.ajax({
    url: '/theme/', // on donne l'URL du fichier de traitement
    timeout: 5000,
    type: "POST", // la requête est de type POST
    data: { "theme": theme }, // et on envoie nos données
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

function depliable(parti) {
  var element = "#content_" + parti;
  var chevron = "#chevron_" + parti;
  if ($(element).is(":visible")) {
    $(element).css("display", "none");
    $(chevron).removeClass("fa-chevron-up");
    $(chevron).addClass("fa-chevron-down");
  }
  else {
    $(element).css("display", "block");
    $(chevron).removeClass("fa-chevron-down");
    $(chevron).addClass("fa-chevron-up");
  }
}

function inputNom() {
  var contenu = $('#nom').html().trim();
  $('#nom').replaceWith('<div style="width:95%;width: calc(100% - 35px); margin-right: 15px; cursor: pointer;" class="input_inscription control has-icons-left has-icons-right"><input autocomplete="off" class="color_input input" placeholder="Nom" name="nom" id="nom" value="' + contenu + '"><span class="icon is-small is-left"><i class="fas fa-user-alt"></i></span><span class="icon is-small is-right"><i class="fas fa-check" id="familyName_check"></i></span></div>'); // remplace le code HTML actuel par celui-ci
  $('#nom').keyup(function() {
    verifNom();
  });
}
function verifNom() {
  var $nom = $('#nom'),
    $familyName_check = $('#familyName_check');
  if ($nom.val().length < 3) { // si la chaîne de caractères est inférieure à 5
    $nom.css({ // on rend le champ rouge
      borderColor: 'red',
      boxShadow: '0 0 0 0.125em #ff000099',
    });
    $familyName_check.removeClass("fas fa-check");
    $familyName_check.addClass("fas fa-times");
    $familyName_check.css({ // on rend le champ rouge
      color: 'red',
    });
    return false;
  } else {
    $nom.css({ // si tout est bon, on le rend vert
      borderColor: 'green',
      boxShadow: '0 0 0 0.125em #00800099',
    });
    $familyName_check.removeClass("fas fa-times");
    $familyName_check.addClass("fas fa-check");
    $familyName_check.css({ // on rend le champ rouge
      color: 'green',
    });
    return true;
  }
}
function inputPrenom() {
  var contenu = $('#prenom').html().trim();
  $('#prenom').replaceWith('<div style="width:95%;width: calc(100% - 35px); margin-right: 15px; cursor: pointer;" class="input_inscription control has-icons-left has-icons-right"><input class="color_input input" placeholder="Prénom" name="prenom" id="prenom" value="' + contenu + '"><span class="icon is-small is-left"><i class="fas fa-user-alt"></i></span><span class="icon is-small is-right"><i class="fas fa-check" id="name_check"></i></span></div>'); // remplace le code HTML actuel par celui-ci
  $('#prenom').keyup(function() {
    verifPrenom();
  });
}
function verifPrenom() {
  var $prenom = $('#prenom'),
    $name_check = $('#name_check');
  if ($prenom.val().length < 2) { // si la chaîne de caractères est inférieure à 5
    $prenom.css({ // on rend le champ rouge
      borderColor: 'red',
      boxShadow: '0 0 0 0.125em #ff000099',
    });
    $name_check.removeClass("fas fa-check");
    $name_check.addClass("fas fa-times");
    $name_check.css({ // on rend le champ rouge
      color: 'red',
    });
    return false;
  } else {
    $prenom.css({ // si tout est bon, on le rend vert
      borderColor: 'green',
      boxShadow: '0 0 0 0.125em #00800099',
    });
    $name_check.removeClass("fas fa-times");
    $name_check.addClass("fas fa-check");
    $name_check.css({ // on rend le champ rouge
      color: 'green',
    });
    return true;
  }
}
function inputPseudo() {
  var contenu = $('#pseudo').html().trim();
  $('#pseudo').replaceWith('<div style="width:95%;width: calc(100% - 35px); margin-right: 15px; cursor: pointer;" class="input_inscription control has-icons-left has-icons-right"><input autocomplete="off" class="color_input input" type="text" placeholder="Pseudo" name="pseudo" id="pseudo" value="' + contenu + '"><span class="icon is-small is-left"><i class="far fa-smile-wink"></i></span><span class="icon is-small is-right"><i class="fas fa-check" id="pseudo_check"></i></span></div>'); // remplace le code HTML actuel par celui-ci
  $('#pseudo').keyup(function() {
    verifPseudo();
  });
}
function verifPseudo() {
  var $pseudo = $('#pseudo'),
    $pseudo_check = $('#pseudo_check');
  if ($pseudo.val().length < 4) { // si la chaîne de caractères est inférieure à 5
    $pseudo.css({ // on rend le champ rouge
      borderColor: 'red',
      boxShadow: '0 0 0 0.125em #ff000099',
    });
    $pseudo_check.removeClass("fas fa-check");
    $pseudo_check.addClass("fas fa-times");
    $pseudo_check.css({ // on rend le champ rouge
      color: 'red',
    });
    return false;
  } else {
    $pseudo.css({ // si tout est bon, on le rend vert
      borderColor: 'green',
      boxShadow: '0 0 0 0.125em #00800099',
    });
    $pseudo_check.removeClass("fas fa-times");
    $pseudo_check.addClass("fas fa-check");
    $pseudo_check.css({ // on rend le champ rouge
      color: 'green',
    });
    return true;
  }
}


function inputMdp() {
  $('#contentmdp').removeClass('contentmdp');
  $('#logoModifieMdp').removeClass('fas fa-pen');
  $('#contentmdp').addClass('contentmdpOn');
  $('#mdp').replaceWith('<div class="content_mdp"><div class="control has-icons-left has-icons-right" style="width: 100%;"><input class="color_input input" type="password" placeholder="Mot de passe" name="password" id="mdp"><span class="icon is-small is-left"><i class="fas fa-lock"></i></span><span class="icon is-small is-right"><i class="fas fa-check" id="password_check"></i></span></div><div class="oeil" onclick="voir(1)"><i id="oeilid" class="fas fa-eye oeil"></i></div></div><div class="progressBar"><div class="progress-done"></div></div><ul id="indiq_verif" class="txt_centre indiq_verif"><li id="taille-mdp"></li><li id="min-mdp"></li><li id="maj-mdp"></li><li id="chiffre-mdp"></li></ul><br /><div class="content_mdp"><div class="control has-icons-left has-icons-right" style="width: 100%;"><input class="color_input input" type="password" placeholder="Confirmation mot de passe" name="confmdp" id="confmdp"><span class="icon is-small is-left"><i class="fas fa-lock"></i></span><span class="icon is-small is-right"><i class="fas fa-check" id="confPassword_check"></i></span></div><div class="oeil" onclick="voir(2)"><i id="oeilid2" class="fas fa-eye oeil"></i></div></div>'); // remplace le code HTML actuel par celui-ci
  $('#mdp').keyup(function() {
    verifMdp();
  });
  $('#confmdp').keyup(function() {
    verifConfMdp();
  });
}

function verifMdp() {
  var $mdp = $('#mdp'),
    $password_check = $('#password_check');
  var pourcent = 0;
  const progress = document.querySelector('.progress-done');
  document.querySelector('.progressBar').style.display = 'none';
  pourcent = 0;
  let barre = $("#barre-mdp");
  barre.children().remove();
  barre.text("");
  let taille = $("#taille-mdp");
  taille.children().remove();
  taille.text("");
  let min = $("#min-mdp");
  min.children().remove();
  min.text("");
  let maj = $("#maj-mdp");
  maj.children().remove();
  maj.text("");
  let digit = $("#chiffre-mdp");
  digit.children().remove();
  digit.text("");
  //Vérifie qu'il y a au moins 8 caractères
  if (/^(.{8,})/.test($mdp.val())) {
    pourcent += 72;
    boul1 = true;
    taille.append('<span style="color: green;"><i class="fas fa-check-circle is-font-primary"></i></span> Au moins 8 caractères. (' + $mdp.val().length + '/8)');
    $('.indiq_verif').addClass('add');
  } else {
    pourcent += ($mdp.val().length) / 8 * 72;
    boul1 = false;
    taille.append('<span style="color: red;"><i class="fas fa-times-circle is-font-danger"></i></span> Au moins 8 caractères. (' + $mdp.val().length + '/8)');
    $('.indiq_verif').addClass('add');
  }
  //Vérification du chiffre
  if (/^(?=.*\d)/.test($mdp.val())) {
    boul2 = true;
    pourcent += 9.4;
    digit.append('<span style="color: green;"><i class="fas fa-check-circle is-font-primary"></i></span> Au moins 1 chiffre.');
  } else {
    boul2 = false;
    digit.append('<span style="color: red;"><i class="fas fa-times-circle is-font-danger"></i></span> Au moins 1 chiffre.');
  }
  //Vérification de la minuscule
  if (/^(?=.*[a-z])/.test($mdp.val())) {
    boul3 = true;
    pourcent += 9.3;
    min.append('<span style="color: green;"><i class="fas fa-check-circle is-font-primary"></i></span> Au moins 1 caractère en minuscule.');
  } else {
    boul3 = false;
    min.append('<span style="color: red;"><i class="fas fa-times-circle is-font-danger"></i></span> Au moins 1 caractère en minuscule.');
  }
  //Vérification de la majuscule
  if (/^(?=.*[A-Z])/.test($mdp.val())) {
    boul4 = true;
    pourcent += 9.3;
    maj.append('<span style="color: green;"><i class="fas fa-check-circle is-font-primary"></i></span> Au moins 1 caractère en majuscule.');
  } else {
    boul4 = false;
    maj.append('<span style="color: red;"><i class="fas fa-times-circle is-font-danger"></i></span> Au moins 1 caractère en majuscule.');
  }
  document.querySelector('.progressBar').style.display = 'block';
  console.log(pourcent);
  var rouge = (100 - pourcent) / 100 * 255;
  var vert = pourcent / 100 * 255;
  progress.style.width = pourcent + '%';
  progress.style.backgroundColor = 'rgb(' + rouge + ',' + vert + ',0)';

  if (boul1 == true && boul2 == true && boul3 == true && boul4 == true) {
    $mdp.css({ // on rend le champ rouge
      borderColor: 'green',
      boxShadow: '0 0 0 0.125em #00800099',
    });
    $password_check.removeClass("fas fa-times");
    $password_check.addClass("fas fa-check");
    $password_check.css({ // on rend le champ rouge
      color: 'green',
    });
    return true;
  } else {
    $mdp.css({ // on rend le champ rouge
      borderColor: 'red',
      boxShadow: '0 0 0 0.125em #ff000099',
    });
    $password_check.removeClass("fas fa-check");
    $password_check.addClass("fas fa-times");
    $password_check.css({ // on rend le champ rouge
      color: 'red',
    });
    return false;
  }
}

function verifConfMdp() {
  var $confmdp = $('#confmdp'),
    $confPassword_check = $('#confPassword_check'),
    $mdp = $('#mdp');
  if ($confmdp.val() != $mdp.val() || $confmdp.val() == '') { // si la confirmation est différente du mot de passe
    $confmdp.css({ // on rend le champ rouge
      borderColor: 'red',
      boxShadow: '0 0 0 0.125em #ff000099',
    });
    $confPassword_check.removeClass("fas fa-check");
    $confPassword_check.addClass("fas fa-times");
    $confPassword_check.css({ // on rend le champ rouge
      color: 'red',
    });
    return false;
  } else {
    $confmdp.css({ // si tout est bon, on le rend vert
      borderColor: 'green',
      boxShadow: '0 0 0 0.125em #00800099',
    });
    $confPassword_check.removeClass("fas fa-times");
    $confPassword_check.addClass("fas fa-check");
    $confPassword_check.css({ // on rend le champ rouge
      color: 'green',
    });
    return true;
  }
}


function inputLycee() {
  var contenu = $('#lycee').html().trim();
  $('#lycee').replaceWith('<div style="width:95%;width: calc(100% - 35px); margin-right: 15px; cursor: pointer;" class="input_inscription control has-icons-left has-icons-right"><input autocomplete="off" class="color_input input" type="text" placeholder="Lycée" id="school" value="' + contenu + '"><span class="icon is-small is-left"><i class="fas fa-school"></i></span><span class="icon is-small is-right"><i class="fas fa-check" id="school_check"></i></span></div><input type="hidden" name="school" id="schoolValue">'); // remplace le code HTML actuel par celui-ci
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
            var lyceeVal = JSON.stringify({ 'nomVille': nomVille, 'id': donnee["records"][i]["fields"]["identifiant_de_l_etablissement"] });
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
        minLength: 0
      });

      if (lycee.indexOf($school.val()) === -1) {
        $school.css({ // on rend le champ rouge
          borderColor: 'red',
          boxShadow: '0 0 0 0.125em #ff000099',
        });
        $school_check.removeClass("fas fa-check");
        $school_check.addClass("fas fa-times");
        $school_check.css({ // on rend le champ rouge
          color: 'red',
        });
        retour = false;
      } else {
        $school.css({ // si tout est bon, on le rend vert
          borderColor: 'green',
          boxShadow: '0 0 0 0.125em #00800099',
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
function closeCont() {
  $('.contenu').removeClass("active"),
    $("#delete").css("zIndex", "1");
  $("#ConfSupp-filtre").css("display", "none");
}
