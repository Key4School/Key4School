$(document).ready(function() {

  var $spe1 = $('#spe1'),
    $spe1_check= $('#spe1_check'),
    $spe2 = $('#spe2'),
    $spe2_check= $('#spe2_check'),
    $spe3 = $('#spe3'),
    $spe3_check= $('#spe3_check'),
    $option1 = $('#option1'),
    $option1_check= $('#option1_check'),
    $option2 = $('#option2'),
    $option2_check= $('#option2_check'),
    $option3 = $('#option3'),
    $option3_check= $('#option3_check'),
    $spes=["Non renseignée...", "Spé Arts", "Spé HGGSP", "Spé HLP", "Spé SES", "Spé Mathématiques", "Spé Physique-Chimie", "Spé SVT", "Spé NSI", "Spé Sciences de l'Ingénieur", "Spé LCA", "Spé LLCER Anglais", "Spé LLCER Espagnol", "Spé LLCER Allemand", "Spé LLCER Italien", "Spé Biologie-écologie"],
    $options=["Non renseignée...", "LCA Latin", "LCA Grec", "LV3 Anglais", "LV3 Espagnol", "LV3 Allemand", "LV3 Portugais", "LV3 Italien", "LV3 Russe", "LV3 Arabe", "LV3 Chinois", "EPS", "Arts", "Musique", "Management et gestion", "Santé et social", "Biotechnologies", "Sciences et laboratoire", "Sciences de l'Ingénieur", "Création et innovation technologiques", "Création et culture - design", "Maths complémentaires", "Maths expertes", "Droits et grands enjeux du monde contemporain", "Hippologie et équitation", "Agronomie-économie-territoires", "Pratiques sociales et culturelles"],
    envoi = $('#envoi'),
    $form = $('#formIncription'),
    $champ = $('.champ'); 

  $spe1.keyup(function() {
    verifSpe1();
  });
  $spe2.keyup(function() {
    verifSpe2();
  });
  $spe3.keyup(function() {
    verifSpe3();
  });
  $option1.keyup(function() {
    verifOption1();
  });
  $option2.keyup(function() {
    verifOption2();
  });
  $option3.keyup(function() {
    verifOption3();
  });

  function verifSpe1() {
    if ($spes.indexOf($spe1.val()) === -1) {
      $spe1.css({ // on rend le champ rouge
        border: '3px solid red',
      });
      $spe1_check.removeClass("fas fa-check");
      $spe1_check.addClass("fas fa-times");
      $spe1_check.css({ // on rend le champ rouge
        color: 'red',
      });
      return false;
    } else {
      $spe1.css({ // si tout est bon, on le rend vert
        border: '3px solid green',
      });
      $spe1_check.removeClass("fas fa-times");
      $spe1_check.addClass("fas fa-check");
      $spe1_check.css({ // on rend le champ rouge
        color: 'green',
      });
      return true;
    }
  }

  function verifSpe2() {
    if ($spes.indexOf($spe2.val()) === -1) {
      $spe2.css({ // on rend le champ rouge
        border: '3px solid red',
      });
      $spe2_check.removeClass("fas fa-check");
      $spe2_check.addClass("fas fa-times");
      $spe2_check.css({ // on rend le champ rouge
        color: 'red',
      });
      return false;
    } else {
      $spe2.css({ // si tout est bon, on le rend vert
        border: '3px solid green',
      });
      $spe2_check.removeClass("fas fa-times");
      $spe2_check.addClass("fas fa-check");
      $spe2_check.css({ // on rend le champ rouge
        color: 'green',
      });
      return true;
    }
  }

  function verifSpe3() {
    if ($spes.indexOf($spe3.val()) === -1) {
      $spe3.css({ // on rend le champ rouge
        border: '3px solid red',
      });
      $spe3_check.removeClass("fas fa-check");
      $spe3_check.addClass("fas fa-times");
      $spe3_check.css({ // on rend le champ rouge
        color: 'red',
      });
      return false;
    } else {
      $spe3.css({ // si tout est bon, on le rend vert
        border: '3px solid green',
      });
      $spe3_check.removeClass("fas fa-times");
      $spe3_check.addClass("fas fa-check");
      $spe3_check.css({ // on rend le champ rouge
        color: 'green',
      });
      return true;
    }
  }

  function verifOption1() {
    if ($options.indexOf($option1.val()) === -1) {
      $option1.css({ // on rend le champ rouge
        border: '3px solid red',
      });
      $option1_check.removeClass("fas fa-check");
      $option1_check.addClass("fas fa-times");
      $option1_check.css({ // on rend le champ rouge
        color: 'red',
      });
      return false;
    } else {
      $option1.css({ // si tout est bon, on le rend vert
        border: '3px solid green',
      });
      $option1_check.removeClass("fas fa-times");
      $option1_check.addClass("fas fa-check");
      $option1_check.css({ // on rend le champ rouge
        color: 'green',
      });
      return true;
    }
  }
  function verifOption2() {
    if ($options.indexOf($option1.val()) === -1) {
      $option2.css({ // on rend le champ rouge
        border: '3px solid red',
      });
      $option2_check.removeClass("fas fa-check");
      $option2_check.addClass("fas fa-times");
      $option2_check.css({ // on rend le champ rouge
        color: 'red',
      });
      return false;
    } else {
      $option2.css({ // si tout est bon, on le rend vert
        border: '3px solid green',
      });
      $option2_check.removeClass("fas fa-times");
      $option2_check.addClass("fas fa-check");
      $option2_check.css({ // on rend le champ rouge
        color: 'green',
      });
      return true;
    }
  }
  function verifOption3() {
    if ($options.indexOf($option3.val()) === -1) {
      $option3.css({ // on rend le champ rouge
        border: '3px solid red',
      });
      $option3_check.removeClass("fas fa-check");
      $option3_check.addClass("fas fa-times");
      $option3_check.css({ // on rend le champ rouge
        color: 'red',
      });
      return false;
    } else {
      $option3.css({ // si tout est bon, on le rend vert
        border: '3px solid green',
      });
      $option3_check.removeClass("fas fa-times");
      $option3_check.addClass("fas fa-check");
      $option3_check.css({ // on rend le champ rouge
        color: 'green',
      });
      return true;
    }
  }

    $envoi.click(function(e) {
       e.preventDefault(); // on annule la fonction par défaut du bouton d'envoi
       // on verifie que le pseudo et l'email n'existe pas encore
       var json;
       $.ajax({
         url: "recupPseudoEmail.php",
         type: "GET",
         dataType: 'json',
         async: false,
         success: function(out) {
           json = out;
         }
       });
        if (verifSpe1() && verifSpe2() && verifSpe3() && verifOption1() && verifOption2() && verifOption3()) {
          $form.submit();
        }else {
          $erreur.html("Vous n'avez pas rempli correctement les champs du formulaire !");// on affiche le message d'erreur
        }
    });
});
