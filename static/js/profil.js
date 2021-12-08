var boul1 = false;
var boul2 = false;
var boul3 = false;
var boul4 = false;
var theme = "";
var champsFaux = [];
var listColor = [{
  'light': ['#00b7ff', '#a7ceff', '#94e1ff', '#d3e6ff'],
  'dark': ['#0a7dff', '#6595d1', '#a4e1f9', '#b2cae8']
},
{
  'light': ['#ff0000', '#ffa8a8', '#ff9494', '#ffd3d3'],
  'dark': ['#bb0404', '#cc0000', '#ff8585', '#e68080']
},
{
  'light': ['#14db14', '#aeffa8', '#a0ff94', '#d6ffd3',],
  'dark': ['#14db14', '#5ab953', '#a0ff94', '#addca9']
},
{
  'light': ['#ffbb00', '#e8c959', '#ffe294', '#f3e4ac'],
  'dark': ['#dfa300', '#c5a73c', '#ffe294', '#ffe68c']
},
{
  'light': ['#e6445f', '#f3a6b3', '#afe2e7', '#f9d3d9'],
  'dark': ['#ff6780', '#cd7d8b', '#afe2e7', '#e6bec5']
},
{
  'light': ['#deb72f', '#e6cf81', '#e68181', '#f3e7c0'],
  'dark': ['#deb72f', '#876e19', '#e68181', '#ffeca9']
},
{
  'light': ['#7a08fa', '#a82ffc', '#d189ff', '#d397fd'],
  'dark': ['#7a08fa', '#a82ffc', '#d189ff', '#d397fd']
},
{
  'light': ['#db3056', '#ff6464', '#ffb99a', '#ffb2b2'],
  'dark': ['#ef6483', '#ff6464', '#ffb99a', '#ffb2b2']
}]
$(document).ready(function() {
  $('#lv1').change(function() {
    verifLangue();
  });
  $('#lv2').change(function() {
    verifLangue();
  });
  $('#option1').change(function() {
    verifOption();
  });
  $('#option2').change(function() {
    verifOption();
  });
  $('#spe1').change(function() {
    verifSpe();
  });
  $('#spe2').change(function() {
    verifSpe();
  });
  $('#spe3').change(function() {
    verifSpe();
  });
  $('#couleur9-1').val(couleur_un);
  $('#couleur9-2').val(couleur_deux);
  $('#couleur9-3').val(couleur_trois);
  $('#pf-delete-ConfSup').click(function() {
    $('.pf-contenu-confSup').addClass("active"),
      $("#pf-delete-ConfSup").css("zIndex", "-1");
    $("#ConfSupp-filtre").css("display", "block");
  });
  $('#updateProfil').submit(function() {
    // if (verifNom() && verifPrenom() && verifPseudo() && verifSchool(false) && verifMdp() && verifConfMdp() && verifPhone() && verifEmail() && verifLangue() && verifOption() && verifSpe()) {
    //   return true;
    // }
    verifNom()
    verifPrenom()
    verifPseudo()
    verifSchool(false)
    verifMdp()
    verifConfMdp()
    verifPhone()
    verifEmail()
    verifLangue()
    verifOption()
    verifSpe()
    if (champsFaux.length == 0) {
      return true;
    }
    else {
      if (champsFaux.length == 1) {
        var adj = "le champ"
      }
      else {
        var adj = "les champs"
      }
      $('#msgErreur').empty();
      $('#msgErreur').css("marginBottom", "3%");
      $('#msgErreur').append("Il y a une erreur avec " + adj + " : " + champsFaux.join(', '))
      return false;
    }
  });

  if (document.documentElement.getAttribute("data-theme") == "dark") {
    $(".sun").addClass("sun-logo");
    $(".moon").addClass("moon-logo");
    theme = "dark"
  }
  if (document.documentElement.getAttribute("data-theme") == "light") {
    $(".sun").addClass("animate-sun");
    $(".moon").addClass("animate-moon");
    theme = "light"
  }
  if (document.documentElement.getAttribute("data-theme") == "system") {
    $("#systemTheme").prop('checked', true);
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      $(".sun").addClass("sun-logo");
      $(".moon").addClass("moon-logo");
      $(".sun").removeClass("animate-sun");
      $(".moon").removeClass("animate-moon");
      theme = "dark"
    } else {
      $(".sun").removeClass("sun-logo");
      $(".moon").removeClass("moon-logo");
      $(".sun").addClass("animate-sun");
      $(".moon").addClass("animate-moon");
      theme = "light"
    }
  }
  $('#couleur1-1').css("backgroundColor", listColor[0][theme][0]);
  $('#couleur1-2').css("backgroundColor", listColor[0][theme][1]);
  $('#couleur1-3').css("backgroundColor", listColor[0][theme][2]);
  $('#couleur2-1').css("backgroundColor", listColor[1][theme][0]);
  $('#couleur2-2').css("backgroundColor", listColor[1][theme][1]);
  $('#couleur2-3').css("backgroundColor", listColor[1][theme][2]);
  $('#couleur3-1').css("backgroundColor", listColor[2][theme][0]);
  $('#couleur3-2').css("backgroundColor", listColor[2][theme][1]);
  $('#couleur3-3').css("backgroundColor", listColor[2][theme][2]);
  $('#couleur4-1').css("backgroundColor", listColor[3][theme][0]);
  $('#couleur4-2').css("backgroundColor", listColor[3][theme][1]);
  $('#couleur4-3').css("backgroundColor", listColor[3][theme][2]);
  $('#couleur5-1').css("backgroundColor", listColor[4][theme][0]);
  $('#couleur5-2').css("backgroundColor", listColor[4][theme][1]);
  $('#couleur5-3').css("backgroundColor", listColor[4][theme][2]);
  $('#couleur6-1').css("backgroundColor", listColor[5][theme][0]);
  $('#couleur6-2').css("backgroundColor", listColor[5][theme][1]);
  $('#couleur6-3').css("backgroundColor", listColor[5][theme][2]);
  $('#couleur7-1').css("backgroundColor", listColor[6][theme][0]);
  $('#couleur7-2').css("backgroundColor", listColor[6][theme][1]);
  $('#couleur7-3').css("backgroundColor", listColor[6][theme][2]);
  $('#couleur8-1').css("backgroundColor", listColor[7][theme][0]);
  $('#couleur8-2').css("backgroundColor", listColor[7][theme][1]);
  $('#couleur8-3').css("backgroundColor", listColor[7][theme][2]);

  // leaderboard selection du top
  $('#lb-france').click(function() {
    $('#lb-france').addClass('is-active');
    $('#lb-depart').removeClass('is-active');
    $('#lb-lycee').removeClass('is-active');
    $.ajax({
      type: 'GET',
      url: '/topLeaderboard/france',
      async: true,
      success: function(result) {
        $("#leaderboard_content").html(result);
      }
    });
  });
  $('#lb-depart').click(function() {
    $('#lb-depart').addClass('is-active');
    $('#lb-france').removeClass('is-active');
    $('#lb-lycee').removeClass('is-active');
    $.ajax({
      type: 'GET',
      url: '/topLeaderboard/departement',
      async: true,
      success: function(result) {
        $("#leaderboard_content").html(result);
      }
    });
  });
  $('#lb-lycee').click(function() {
    $('#lb-lycee').addClass('is-active');
    $('#lb-france').removeClass('is-active');
    $('#lb-depart').removeClass('is-active');
    $.ajax({
      type: 'GET',
      url: '/topLeaderboard/lycee',
      async: true,
      success: function(result) {
        $("#leaderboard_content").html(result);
      }
    });
  });
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
    if (champsFaux.indexOf("nom") === -1) {
      champsFaux.push('nom');
    }

    // return false;
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
    const index = champsFaux.indexOf("nom");
    if (index > -1) {
      champsFaux.splice(index, 1);
    }
    // return true;
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
    if (champsFaux.indexOf("prénom") === -1) {
      champsFaux.push('prénom');
    }
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
    const index = champsFaux.indexOf("prénom");
    if (index > -1) {
      champsFaux.splice(index, 1);
    }
    // return true;
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
    if (champsFaux.indexOf("pseudo") === -1) {
      champsFaux.push('pseudo');
    }
    // return false;
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
    const index = champsFaux.indexOf("pseudo");
    if (index > -1) {
      champsFaux.splice(index, 1);
    }
    // return true;
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
    // return true;
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
      const index = champsFaux.indexOf("mot de passe");
      if (index > -1) {
        champsFaux.splice(index, 1);
      }
      // return true;
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
      if (champsFaux.indexOf("mot de passe") === -1) {
        champsFaux.push('mot de passe');
      }
      // return false;
    }
  }

}

function verifConfMdp() {
  if ($('#mdp').get(0).tagName == 'P') {
    // return true;
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
      if (champsFaux.indexOf("confirmation de mot de passe") === -1) {
        champsFaux.push('confirmation de mot de passe');
      }
      // return false;
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
      const index = champsFaux.indexOf("confirmation de mot de passe");
      if (index > -1) {
        champsFaux.splice(index, 1);
      }
      // return true;
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
  if ($('#school').get(0).tagName == 'P') {
    $('#hiddenLycee').val('');
    // return true;
  }
  else {
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
          if (champsFaux.indexOf("lycée") === -1) {
            champsFaux.push('lycée');
          }
          // retour = false;
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
          const index = champsFaux.indexOf("lycée");
          if (index > -1) {
            champsFaux.splice(index, 1);
          }
          // retour = true;
        }
      }
    });
  }
  // return retour;
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
    if (champsFaux.indexOf("email") === -1) {
      champsFaux.push('email');
    }
    // return false;
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
    const index = champsFaux.indexOf("email");
    if (index > -1) {
      champsFaux.splice(index, 1);
    }
    // return true;
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
      if (champsFaux.indexOf("téléphone") === -1) {
        champsFaux.push('téléphone');
      }
      // return false;
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
      const index = champsFaux.indexOf("téléphone");
      if (index > -1) {
        champsFaux.splice(index, 1);
      }
      // return true;
    }
  }
}

function verifLangue() {
  const lv1 = $('#lv1').val().split('-');
  const lv2 = $('#lv2').val().split('-');
  if (lv1[1] == lv2[1]) {
    $('#lv1').css({ // si tout est bon, on le rend vert
      borderColor: 'red',
      boxShadow: '0 0 0 0.125em #ff000099',
    });
    $('#lv2').css({ // si tout est bon, on le rend vert
      borderColor: 'red',
      boxShadow: '0 0 0 0.125em #ff000099',
    });
    if (champsFaux.indexOf("langues") === -1) {
      champsFaux.push('langues');
    }

    // return false;
  }
  else {
    $('#lv1').css({ // si tout est bon, on le rend vert
      borderColor: 'green',
      boxShadow: '0 0 0 0.125em #00800099',
    });
    $('#lv2').css({ // si tout est bon, on le rend vert
      borderColor: 'green',
      boxShadow: '0 0 0 0.125em #00800099',
    });
    const index = champsFaux.indexOf("langues");
    if (index > -1) {
      champsFaux.splice(index, 1);
    }
    // return true;
  }
}

function verifOption() {
  const option1 = $('#option1').val().split('-');
  const option2 = $('#option2').val().split('-');
  if (option1[1] == option2[1]) {
    $('#option1').css({ // si tout est bon, on le rend vert
      borderColor: 'red',
      boxShadow: '0 0 0 0.125em #ff000099',
    });
    $('#option2').css({ // si tout est bon, on le rend vert
      borderColor: 'red',
      boxShadow: '0 0 0 0.125em #ff000099',
    });
    if (champsFaux.indexOf("options") === -1) {
      champsFaux.push('options');
    }

    // return false;
  }
  else {
    $('#option1').css({ // si tout est bon, on le rend vert
      borderColor: 'green',
      boxShadow: '0 0 0 0.125em #00800099',
    });
    $('#option2').css({ // si tout est bon, on le rend vert
      borderColor: 'green',
      boxShadow: '0 0 0 0.125em #00800099',
    });
    const index = champsFaux.indexOf("options");
    if (index > -1) {
      champsFaux.splice(index, 1);
    }
    // return true;
  }
}

function verifSpe() {
  if (classe == '1G') {
    const spe1 = $('#spe1').val().split('-');
    const spe2 = $('#spe2').val().split('-');
    const spe3 = $('#spe3').val().split('-');
    if (spe1[1] == spe2[1] || spe1[1] == spe3[1] || spe3[1] == spe2[1]) {
      $('#spe1').css({ // si tout est bon, on le rend vert
        borderColor: 'red',
        boxShadow: '0 0 0 0.125em #ff000099',
      });
      $('#spe2').css({ // si tout est bon, on le rend vert
        borderColor: 'red',
        boxShadow: '0 0 0 0.125em #ff000099',
      });
      $('#spe3').css({ // si tout est bon, on le rend vert
        borderColor: 'red',
        boxShadow: '0 0 0 0.125em #ff000099',
      });
      if (champsFaux.indexOf("spécialités") === -1) {
        champsFaux.push('spécialités');
      }

      // return false;
    }
    else {
      $('#spe1').css({ // si tout est bon, on le rend vert
        borderColor: 'green',
        boxShadow: '0 0 0 0.125em #00800099',
      });
      $('#spe2').css({ // si tout est bon, on le rend vert
        borderColor: 'green',
        boxShadow: '0 0 0 0.125em #00800099',
      });
      $('#spe3').css({ // si tout est bon, on le rend vert
        borderColor: 'green',
        boxShadow: '0 0 0 0.125em #00800099',
      });
      const index = champsFaux.indexOf("spécialités");
      if (index > -1) {
        champsFaux.splice(index, 1);
      }
      // return true;
    }
  }
  if (classe == 'TG') {
    const spe1 = $('#spe1').val().split('-');
    const spe2 = $('#spe2').val().split('-');
    if (spe1[1] == spe2[1]) {
      $('#spe1').css({ // si tout est bon, on le rend vert
        borderColor: 'red',
        boxShadow: '0 0 0 0.125em #ff000099',
      });
      $('#spe1').css({ // si tout est bon, on le rend vert
        borderColor: 'red',
        boxShadow: '0 0 0 0.125em #ff000099',
      });
      if (champsFaux.indexOf("nom") === -1) {
        champsFaux.push('spécialités');
      }
      // return false;
    }
    else {
      $('#spe1').css({ // si tout est bon, on le rend vert
        borderColor: 'green',
        boxShadow: '0 0 0 0.125em #00800099',
      });
      $('#spe2').css({ // si tout est bon, on le rend vert
        borderColor: 'green',
        boxShadow: '0 0 0 0.125em #00800099',
      });
      const index = champsFaux.indexOf("spécialités");
      if (index > -1) {
        champsFaux.splice(index, 1);
      }
      // return true;
    }
  }
}


function updateImgOpen() {
  $("#replaceImg").addClass("is-active");
}

function updateImgClose() {
  $("#replaceImg").removeClass("is-active");
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
