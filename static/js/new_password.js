$(document).ready(function() {

  var $pseudo_check= $mdp = $('#mdp'),
    $password_check= $('#password_check'),
    $confmdp = $('#confmdp'),
    $confPassword_check= $('#confPassword_check'),
    $form = $('#form'),
    $erreur = $('#erreur');

  $erreur.css({
    display: 'none',
  });

  var pourcent = 0;
  var boul1 = false;
  var boul2 = false;
  var boul3 = false;
  var boul4 = false;
  const progress = document.querySelector('.progress-done');
  document.querySelector('.progressBar').style.display = 'none';

  $mdp.keyup(function() {
    verifMdp();
  });
  $confmdp.keyup(function() {
    verifConfMdp();
  });


  function verifMdp() {
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
        border: '3px solid green',
      });
      $password_check.removeClass("fas fa-times");
      $password_check.addClass("fas fa-check");
      $password_check.css({ // on rend le champ rouge
        color: 'green',
      });
      return true;
    } else {
      $mdp.css({ // on rend le champ rouge
        border: '3px solid red',
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
    if ($confmdp.val() != $mdp.val() || $confmdp.val() == '') { // si la confirmation est différente du mot de passe
      $confmdp.css({ // on rend le champ rouge
        border: '3px solid red',
      });
      $confPassword_check.removeClass("fas fa-check");
      $confPassword_check.addClass("fas fa-times");
      $confPassword_check.css({ // on rend le champ rouge
        color: 'red',
      });
      return false;
    } else {
      $confmdp.css({ // si tout est bon, on le rend vert
        border: '3px solid green',
      });
      $confPassword_check.removeClass("fas fa-times");
      $confPassword_check.addClass("fas fa-check");
      $confPassword_check.css({ // on rend le champ rouge
        color: 'green',
      });
      return true;
    }
  }


  $form.on('submit', function() {
    if (verifConfMdp() && verifEmail()) {
      return true;
    } else {
      $erreur.css({
        display: 'block',
      });
      return false;
    }
  });
});
