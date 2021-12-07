var boul1 = false;
var boul2 = false;
var boul3 = false;
var boul4 = false;
$(document).ready(function() {
  $('#pf-delete-ConfSup').click(function() {
    $('.pf-contenu-confSup').addClass("active"),
      $("#pf-delete-ConfSup").css("zIndex", "-1");
    $("#ConfSupp-filtre").css("display", "block");
  });
  $('#updateProfil').submit(function() {
    if (verifNom() && verifPrenom() && verifPseudo() && verifSchool(false) && verifMdp() && verifConfMdp() && verifPhone() && verifEmail()) {
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
  $('#hiddenNom').remove();
  $('#penNom').remove();
  $('#nom').replaceWith('<div style="width:100%; cursor: pointer;" class="input_inscription control has-icons-left has-icons-right"><input autocomplete="off" class="color_input input" placeholder="Nom" name="nom" id="nom" value="' + contenu + '"><span class="icon is-small is-left"><i class="fas fa-user-alt"></i></span><span class="icon is-small is-right"><i class="fas fa-check" id="familyName_check"></i></span></div>'); // remplace le code HTML actuel par celui-ci
  $('#nom').keyup(function() {
    verifNom();
  });
}
function verifNom() {
  if ($('#nom').val() == '') {
    var $content_nom = $('#nom').html().trim();
  }
  else {
    var $content_nom = $('#nom').val();
  }
  var $nom = $('#nom'),
    $familyName_check = $('#familyName_check');
  if ($content_nom.length < 3) { // si la chaîne de caractères est inférieure à 5
    if ($nom.get(0).tagName == 'INPUT') {
      $nom.css({ // on rend le champ rouge
        borderColor: 'red',
        boxShadow: '0 0 0 0.125em #ff000099',
      });
      $familyName_check.removeClass("fas fa-check");
      $familyName_check.addClass("fas fa-times");
      $familyName_check.css({ // on rend le champ rouge
        color: 'red',
      });
    }

    return false;
  } else {
    if ($nom.get(0).tagName == 'INPUT') {
      $nom.css({ // si tout est bon, on le rend vert
        borderColor: 'green',
        boxShadow: '0 0 0 0.125em #00800099',
      });
      $familyName_check.removeClass("fas fa-times");
      $familyName_check.addClass("fas fa-check");
      $familyName_check.css({ // on rend le champ rouge
        color: 'green',
      });
    }
    return true;
  }
}
function inputPrenom() {
  $('#penPrenom').remove();
  $('#hiddenPrenom').remove();
  var contenu = $('#prenom').html().trim();
  $('#prenom').replaceWith('<div style="width:100%; cursor: pointer;" class="input_inscription control has-icons-left has-icons-right"><input class="color_input input" placeholder="Prénom" name="prenom" id="prenom" value="' + contenu + '"><span class="icon is-small is-left"><i class="fas fa-user-alt"></i></span><span class="icon is-small is-right"><i class="fas fa-check" id="name_check"></i></span></div>'); // remplace le code HTML actuel par celui-ci
  $('#prenom').keyup(function() {
    verifPrenom();
  });
}
function verifPrenom() {
  if ($('#prenom').val() == '') {
    var $content_prenom = $('#prenom').html().trim();
  }
  else {
    var $content_prenom = $('#prenom').val();
  }
  var $prenom = $('#prenom'),
    $name_check = $('#name_check');
  if ($content_prenom.length < 2) { // si la chaîne de caractères est inférieure à 5
    if ($prenom.get(0).tagName == 'INPUT') {
      $prenom.css({ // on rend le champ rouge
        borderColor: 'red',
        boxShadow: '0 0 0 0.125em #ff000099',
      });
      $name_check.removeClass("fas fa-check");
      $name_check.addClass("fas fa-times");
      $name_check.css({ // on rend le champ rouge
        color: 'red',
      });
    }
    return false;
  } else {
    if ($prenom.get(0).tagName == 'INPUT') {
      $prenom.css({ // si tout est bon, on le rend vert
        borderColor: 'green',
        boxShadow: '0 0 0 0.125em #00800099',
      });
      $name_check.removeClass("fas fa-times");
      $name_check.addClass("fas fa-check");
      $name_check.css({ // on rend le champ rouge
        color: 'green',
      });
    }
    return true;
  }
}
function inputPseudo() {
  $('#hiddenPseudo').remove();
  $('#penPseudo').remove();
  var contenu = $('#pseudo').html().trim();
  $('#pseudo').replaceWith('<div style="width:100%; cursor: pointer;" class="input_inscription control has-icons-left has-icons-right"><input autocomplete="off" class="color_input input" type="text" placeholder="Pseudo" name="pseudo" id="pseudo" value="' + contenu + '"><span class="icon is-small is-left"><i class="far fa-smile-wink"></i></span><span class="icon is-small is-right"><i class="fas fa-check" id="pseudo_check"></i></span></div>'); // remplace le code HTML actuel par celui-ci
  $('#pseudo').keyup(function() {
    verifPseudo();
  });
}
function verifPseudo() {
  if ($('#pseudo').val() == '') {
    var $content_pseudo = $('#pseudo').html().trim();
  }
  else {
    var $content_pseudo = $('#pseudo').val();
  }
  var $pseudo = $('#pseudo'),
    $pseudo_check = $('#pseudo_check');
  if ($content_pseudo.length < 4) { // si la chaîne de caractères est inférieure à 5
    if ($pseudo.get(0).tagName == 'INPUT') {
      $pseudo.css({ // on rend le champ rouge
        borderColor: 'red',
        boxShadow: '0 0 0 0.125em #ff000099',
      });
      $pseudo_check.removeClass("fas fa-check");
      $pseudo_check.addClass("fas fa-times");
      $pseudo_check.css({ // on rend le champ rouge
        color: 'red',
      });
    }
    return false;
  } else {
    if ($pseudo.get(0).tagName == 'INPUT') {
      $pseudo.css({ // si tout est bon, on le rend vert
        borderColor: 'green',
        boxShadow: '0 0 0 0.125em #00800099',
      });
      $pseudo_check.removeClass("fas fa-times");
      $pseudo_check.addClass("fas fa-check");
      $pseudo_check.css({ // on rend le champ rouge
        color: 'green',
      });
    }
    return true;
  }
}


function inputMdp() {
  $('#hiddenMdp').remove();
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
  if ($('#mdp').get(0).tagName == 'P') {
    return true;
  }
  else {
    var $content_mdp = $('#mdp').val();
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

    if (/^(.{8,})/.test($content_mdp)) {
      pourcent += 72;
      boul1 = true;
      taille.append('<span style="color: green;"><i class="fas fa-check-circle is-font-primary"></i></span> Au moins 8 caractères. (' + $content_mdp.length + '/8)');
      $('.indiq_verif').addClass('add');
    } else {
      pourcent += ($content_mdp.length) / 8 * 72;
      boul1 = false;
      taille.append('<span style="color: red;"><i class="fas fa-times-circle is-font-danger"></i></span> Au moins 8 caractères. (' + $content_mdp.length + '/8)');
      $('.indiq_verif').addClass('add');
    }
    //Vérification du chiffre
    if (/^(?=.*\d)/.test($content_mdp)) {
      boul2 = true;
      pourcent += 9.4;
      digit.append('<span style="color: green;"><i class="fas fa-check-circle is-font-primary"></i></span> Au moins 1 chiffre.');
    } else {
      boul2 = false;
      digit.append('<span style="color: red;"><i class="fas fa-times-circle is-font-danger"></i></span> Au moins 1 chiffre.');
    }
    //Vérification de la minuscule
    if (/^(?=.*[a-z])/.test($content_mdp)) {
      boul3 = true;
      pourcent += 9.3;
      min.append('<span style="color: green;"><i class="fas fa-check-circle is-font-primary"></i></span> Au moins 1 caractère en minuscule.');
    } else {
      boul3 = false;
      min.append('<span style="color: red;"><i class="fas fa-times-circle is-font-danger"></i></span> Au moins 1 caractère en minuscule.');
    }
    //Vérification de la majuscule
    if (/^(?=.*[A-Z])/.test($content_mdp)) {
      boul4 = true;
      pourcent += 9.3;
      maj.append('<span style="color: green;"><i class="fas fa-check-circle is-font-primary"></i></span> Au moins 1 caractère en majuscule.');
    } else {
      boul4 = false;
      maj.append('<span style="color: red;"><i class="fas fa-times-circle is-font-danger"></i></span> Au moins 1 caractère en majuscule.');
    }
    document.querySelector('.progressBar').style.display = 'block';
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

}

function verifConfMdp() {
  if ($('#mdp').get(0).tagName == 'P') {
    return true;
  }
  else {
    if ($('#confmdp').val() == '' || $('#confmdp').val() == undefined) {
      var $content_confmdp = $('#confmdp').html().trim();
    }
    else {
      var $content_confmdp = $('#confmdp').val();
    }
    if ($('#mdp').val() == '') {
      var $content_mdp = $('#mdp').html().trim();
    }
    else {
      var $content_mdp = $('#mdp').val();
    }
    var $confmdp = $('#confmdp'),
      $confPassword_check = $('#confPassword_check');
    if ($content_confmdp != $content_mdp || $content_confmdp == '') { // si la confirmation est différente du mot de passe
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

}


function inputLycee() {
  $('#penLycee').remove();
  $('#hiddenLycee').remove();
  var contenu = $('#school').html().trim();
  $('#school').replaceWith('<div style="width:100%; cursor: pointer;" class="input_inscription control has-icons-left has-icons-right"><input autocomplete="off" class="color_input input" type="text" placeholder="Lycée" id="school" value="' + contenu + '"><span class="icon is-small is-left"><i class="fas fa-school"></i></span><span class="icon is-small is-right"><i class="fas fa-check" id="school_check"></i></span></div><input type="hidden" name="school" id="schoolValue">'); // remplace le code HTML actuel par celui-ci
  $('#school').on('change keyup focus', function() {
    verifSchool(true);
  });
}

function verifSchool(asynch) {
  if ($('#school').val() == '' || $('#school').val() == undefined) {
    var $content_school = $('#school').html().trim();
  }
  else {
    var $content_school = $('#school').val();
  }
  var $school = $('#school'),
    $school_check = $('#school_check');
  var retour;
  $.ajax({
    url: 'https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-en-annuaire-education&facet=nom_etablissement&facet=nom_commune&refine.type_etablissement=Lycée',
    dataType: 'json',
    async: asynch,
    data: {
      q: $content_school
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

      if (lycee.indexOf($content_school) === -1) {
        if ($school.get(0).tagName == 'INPUT') {
          $school.css({ // on rend le champ rouge
            borderColor: 'red',
            boxShadow: '0 0 0 0.125em #ff000099',
          });
          $school_check.removeClass("fas fa-check");
          $school_check.addClass("fas fa-times");
          $school_check.css({ // on rend le champ rouge
            color: 'red',
          });
        }
        retour = false;
      } else {
        if ($school.get(0).tagName == 'INPUT') {
          $school.css({ // si tout est bon, on le rend vert
            borderColor: 'green',
            boxShadow: '0 0 0 0.125em #00800099',
          });
          $school_check.removeClass("fas fa-times");
          $school_check.addClass("fas fa-check");
          $school_check.css({ // on rend le champ rouge
            color: 'green',
          });
        }
        $('#schoolValue').val(lyceesValues[$content_school]);
        retour = true;
      }
    }
  });
  return retour;
}


function input(type) {
  $('#hidden' + type).remove();
  $('#pen' + type).remove();
  var contenu = $('#' + type).html().trim();
  if (type == "email") {
    $('#' + type).replaceWith('<div style="width:100%; cursor: pointer;" class="input_inscription control has-icons-left has-icons-right"><input autocomplete="off" class="color_input input" type="text" placeholder="Email" name="email" id="email" value="' + contenu + '"><span class="icon is-small is-left"><i class="fas fa-envelope"></i></span><span class="icon is-small is-right"><i class="fas fa-check" id="email_check"></i></span></div>');
  }
  if (type == "telephone") {
    $('#' + type).replaceWith('<div style="width:100%; cursor: pointer;" class="input_inscription control has-icons-left has-icons-right"><input autocomplete="off" class="color_input input" type="tel" placeholder="(Téléphone) facultatif" name="telephone" id="telephone" value="' + contenu + '"><span class="icon is-small is-left"><i class="fas fa-phone-alt"></i></span><span class="icon is-small is-right"><i class="fas fa-check" id="phone_check"></i></span></div>');
  }
  if (type == "interets") {
    $('#' + type).replaceWith('<div style="width:100%; cursor: pointer;" class="input_inscription control has-icons-left"><input autocomplete="off" class="color_input input" type="text" placeholder="Interets" name="interets" id="interets" value="' + contenu + '"><span class="icon is-small is-left"><i class="far fa-smile-beam"></i></span><span class="icon is-small is-right"></span></div>');
  }
  $('#email').keyup(function() {
    verifEmail();
  });
  $('#telephone').keyup(function() {
    verifPhone();
  });
  $('#interets').keyup(function() {
    verifInterets();
  });
}

function verifEmail() {
  var $email = $("#email"),
    $email_check = $('email_check');
  if ($('#email').val() == '') {
    var $content_email = $('#email').html().trim();
  }
  else {
    var $content_email = $('#email').val();
  }
  var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
  var emailblockReg = /^([\w-\.]+@(?!yopmail.com)([\w-]+\.)+[\w-]{2,4})?$/;
  var emailaddressVal = $content_email;

  if (!emailReg.test(emailaddressVal) || !emailblockReg.test(emailaddressVal) || emailaddressVal == '') {
    if ($email.get(0).tagName == 'INPUT') {
      $email.css({ // si tout est bon, on le rend vert
        borderColor: 'red',
        boxShadow: '0 0 0 0.125em #ff000099',
      });
      $email_check.removeClass("fas fa-check");
      $email_check.addClass("fas fa-times");
      $email_check.css({ // on rend le champ rouge
        color: 'red',
      });
    }
    return false;
  } else {
    if ($email.get(0).tagName == 'INPUT') {
      $email.css({ // si tout est bon, on le rend vert
        borderColor: 'green',
        boxShadow: '0 0 0 0.125em #00800099',
      });
      $email_check.removeClass("fas fa-times");
      $email_check.addClass("fas fa-check");
      $email_check.css({ // on rend le champ rouge
        color: 'green',
      });
    }
    return true;
  }
}

function verifPhone() {
  if ($('#telephone').val() == '') {
    var $content_telephone = $('#telephone').html().trim();
  }
  else {
    var $content_telephone = $('#telephone').val();
  }
  if ($content_telephone == 'Non-renseigné') {
    $('#telephone').val("");
    return true
  }
  else {
    var $phone = $("#telephone"),
      $phone_check = $('phone_check');
    var phoneReg = /^(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})$/;
    var phoneVal = $content_telephone;

    if (!phoneReg.test(phoneVal) & phoneVal != '') {
      if ($phone.get(0).tagName == 'INPUT') {
        $phone.css({ // si tout est bon, on le rend vert
          borderColor: 'red',
          boxShadow: '0 0 0 0.125em #ff000099',
        });
        $phone_check.removeClass("fas fa-check");
        $phone_check.addClass("fas fa-times");
        $phone_check.css({ // on rend le champ rouge
          color: 'red',
        });
      }
      return false;
    } else {
      if ($phone.get(0).tagName == 'INPUT') {
        $phone.css({ // si tout est bon, on le rend vert
          borderColor: 'green',
          boxShadow: '0 0 0 0.125em #00800099',
        });
        $phone_check.removeClass("fas fa-times");
        $phone_check.addClass("fas fa-check");
        $phone_check.css({ // on rend le champ rouge
          color: 'green',
        });
      }
      return true;
    }
  }
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
  $('.pf-contenu-confSup').removeClass("active"),
    $("#pf-delete-ConfSup").css("zIndex", "1");
  $("#ConfSupp-filtre").css("display", "none");
}
