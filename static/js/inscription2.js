$(document).ready(function() {

  var $spe1 = $('#spe1'),
    $spe1_check = $('#spe1_check'),
    $spe2 = $('#spe2'),
    $spe2_check = $('#spe2_check'),
    $spe3 = $('#spe3'),
    $spe3_check = $('#spe3_check'),
    $option1 = $('#option1'),
    $option1_check = $('#option1_check'),
    $option2 = $('#option2'),
    $option2_check = $('#option2_check'),
    $option3 = $('#option3'),
    $option3_check = $('#option3_check'),
    $spes = ["Spé Arts", "Spé HGGSP", "Spé HLP", "Spé SES", "Spé Mathématiques", "Spé Physique-Chimie", "Spé SVT", "Spé NSI", "Spé Sciences de l'Ingénieur", "Spé LCA", "Spé LLCER Anglais", "Spé LLCER Espagnol", "Spé LLCER Allemand", "Spé LLCER Italien", "Spé Biologie-écologie"],
    $options = ["LCA Latin", "LCA Grec", "LV3 Anglais", "LV3 Espagnol", "LV3 Allemand", "LV3 Portugais", "LV3 Italien", "LV3 Russe", "LV3 Arabe", "LV3 Chinois", "EPS", "Arts", "Musique", "Management et gestion", "Santé et social", "Biotechnologies", "Sciences et laboratoire", "Sciences de l'Ingénieur", "Création et innovation technologiques", "Création et culture - design", "Maths complémentaires", "Maths expertes", "Droits et grands enjeux du monde contemporain", "Hippologie et équitation", "Agronomie-économie-territoires", "Pratiques sociales et culturelles"],
    $form = $('#form'),
    $erreur = $('#erreur');

  var speValues = {"Spé Arts": "spe-art",
                  "Spé HGGSP": "spe-hggsp",
                  "Spé HLP": "spe-hlp",
                  "Spé SES": "spe-ses",
                  "Spé Mathématiques": "spe-maths",
                  "Spé Physique-Chimie": "spe-pc",
                  "Spé SVT": "spe-svt",
                  "Spé NSI": "spe-nsi",
                  "Spé Sciences de l'Ingénieur": "spe-si",
                  "Spé LCA": "spe-lca",
                  "Spé LLCER Anglais": "spe-llcer-ang",
                  "Spé LLCER Espagnol": "spe-llcer-esp",
                  "Spé LLCER Allemand": "spe-llcer-all",
                  "Spé LLCER Italien": "spe-llcer-it",
                  "Spé Biologie-écologie": "spe-bio-eco"}

  var optionValues = {"LCA Latin": "opt-lca-latin",
                      "LCA Grec": "opt-lca-grec",
                      "LV3 Anglais": "opt-lv3-ang",
                      "LV3 Espagnol": "opt-lv3-esp",
                      "LV3 Allemand": "opt-lv3-all",
                      "LV3 Portugais": "opt-lv3-por",
                      "LV3 Italien": "opt-lv3-it",
                      "LV3 Russe": "opt-lv3-ru",
                      "LV3 Arabe": "opt-lv3-ara",
                      "LV3 Chinois": "opt-lv3-chi",
                      "EPS": "opt-eps",
                      "Arts": "opt-arts",
                      "Musique": "opt-musique",
                      "Management et gestion": "opt-mg",
                      "Santé et social": "opt-ss",
                      "Biotechnologies": "opt-biotech",
                      "Sciences et laboratoire": "opt-sl",
                      "Sciences de l'Ingénieur": "opt-si",
                      "Création et innovation technologiques": "opt-cit",
                      "Création et culture - design": "opt-ccd",
                      "Maths complémentaires": "opt-maths-comp",
                      "Maths expertes": "opt-maths-exp",
                      "Droits et grands enjeux du monde contemporain": "opt-dgemc",
                      "Hippologie et équitation": "opt-equit",
                      "Agronomie-économie-territoires": "opt-aet",
                      "Pratiques sociales et culturelles": "opt-psc"}

  $erreur.css({ // on rend le champ rouge
    display: 'none',
  });

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
    if($spe1.length == 0) return true;
    if ($spes.indexOf($spe1.val()) === -1 || $spe1.val() == $spe2.val() || $spe1.val() == $spe3.val()) {
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
      $('#spe1Value').val(speValues[$spe1.val()]);
      return true;
    }
  }

  function verifSpe2() {
    if($spe2.length == 0) return true;
    if ($spes.indexOf($spe2.val()) === -1 || $spe2.val() == $spe1.val() || $spe2.val() == $spe3.val()) {
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
      $('#spe2Value').val(speValues[$spe2.val()]);
      return true;
    }
  }

  function verifSpe3() {
    if($spe3.length == 0) return true;
    if ($spes.indexOf($spe3.val()) === -1 || $spe3.val() == $spe1.val() || $spe3.val() == $spe2.val()) {
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
      $('#spe3Value').val(speValues[$spe3.val()]);
      return true;
    }
  }

  function verifOption1() {
    if (($options.indexOf($option1.val()) === -1 || $option1.val() == $option2.val() || $option1.val() == $option3.val())  && $option3.val() != '') {
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
      $('#option1Value').val(optionValues[$option1.val()]);
      return true;
    }
  }

  function verifOption2() {
    if ($options.indexOf(($option1.val()) === -1 || $option2.val() == $option1.val() || $option2.val() == $option3.val())  && $option3.val() != '') {
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
      $('#option2Value').val(optionValues[$option2.val()]);
      return true;
    }
  }

  function verifOption3() {
    if ($options.indexOf(($option3.val()) === -1 || $option3.val() == $option1.val() || $option3.val() == $option2.val()) && $option3.val() != '') {
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
      $('#option3Value').val(optionValues[$option3.val()]);
      return true;
    }
  }

  $form.on('submit', function(e) {
    if (verifSpe1() && verifSpe2() && verifSpe3() && verifOption1() && verifOption2() && verifOption3()) {
      return true;
    } else {
      $erreur.css({
        display: 'block',
      });
      return false;
    }
  });
});
