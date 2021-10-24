$(document).ready(function() {

  var $phone = $('#phone'),
    $phone_check = $('#phone_check'),
    $birthday = $('#birthday'),
    $birthday_check = $('#birthday_check'),
    $school = $('#school'),
    $school_check = $('#school_check'),
    $classe = $('#classe'),
    $classe_check = $('#classe_check'),
    $lva = $('#LVA'),
    $lva_check = $('#LVA_check'),
    $lva_template = $('#template_lva'),
    $lvb = $('#LVB'),
    $lvb_check = $('#LVB_check'),
    $lvb_template = $('#template_lvb'),
    $form = $('#form'),
    $erreur = $('#erreur');

  var langValue = {
    "Anglais": "-ang",
    "Anglais Euro": "-ang-euro",
    "Espagnol": "-esp",
    "Espagnol Euro": "-esp-euro",
    "Allemand": "-all",
    "Allemand Euro": "-all-euro",
    "Portugais": "-por",
    "Portugais Euro": "-por-euro",
    "Itlien": "-it",
    "Itlien Euro": "-it-euro",
    "Chinois": "-chi",
    "Russe": "-ru",
    "Arabe": "-ara",
    "Basque": "-bas",
    "Catalan": "-cat",
    "Créole": "-cre",
    "Hébreu": "-heb",
    "Kanak": "-kan"
  }

  $erreur.css({ // on rend le champ rouge
    display: 'none',
  });

  $phone.keyup(function() {
    verifPhone();
  });
  $birthday.keyup(function() {
    verifBirthday();
  });
  $school.on('change keyup focus', function() {
    verifSchool(true);
  });
  $classe.change(function() {
    verifClasse();
  });
  $lva.keyup(function() {
    verifLva();
  });
  $lvb.keyup(function() {
    verifLvb();
  });

  function verifPhone() {
    var phoneReg = /^(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})$/;
    var phoneVal = $phone.val();

    if (!phoneReg.test(phoneVal) & phoneVal != '') {
      $phone.css({ // si tout est bon, on le rend vert
        borderColor: 'red',
        boxShadow: '0 0 0 0.125em #ff000099',
      });
      $phone_check.removeClass("fas fa-check");
      $phone_check.addClass("fas fa-times");
      $phone_check.css({ // on rend le champ rouge
        color: 'red',
      });
      return false;
    } else {
      $phone.css({ // si tout est bon, on le rend vert
        borderColor: 'green',
        boxShadow: '0 0 0 0.125em #00800099',
      });
      $phone_check.removeClass("fas fa-times");
      $phone_check.addClass("fas fa-check");
      $phone_check.css({ // on rend le champ rouge
        color: 'green',
      });
      return true;
    }
  }

  function verifBirthday() {
    var birthdayReg = /^[12][09][0-9]{2}-\d{2}-\d{2}$/;
    var birthdayVal = $birthday.val();

    if (!birthdayReg.test(birthdayVal) || birthdayVal == '') {
      $birthday.css({ // on rend le champ rouge
        borderColor: 'red',
        boxShadow: '0 0 0 0.125em #ff000099',
      });
      $birthday_check.removeClass("fas fa-check");
      $birthday_check.addClass("fas fa-times");
      $birthday_check.css({ // on rend le champ rouge
        color: 'red',
      });
      return false;
    } else {
      $birthday.css({ // si tout est bon, on le rend vert
        borderColor: 'green',
        boxShadow: '0 0 0 0.125em #00800099',
      });
      $birthday_check.removeClass("fas fa-times");
      $birthday_check.addClass("fas fa-check");
      $birthday_check.css({ // on rend le champ rouge
        color: 'green',
      });
      return true;
    }
  }


  function verifSchool(asynch) {
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

function verifClasse() {
  var classeNone = "--Niveau--";

  var classeVal = $classe.val();

  if (classeVal == classeNone) {
    $classe.css({ // on rend le champ rouge
      borderColor: 'red',
        boxShadow: '0 0 0 0.125em #ff000099',
    });
    $classe_check.removeClass("fas fa-check");
    $classe_check.addClass("fas fa-times");
    $classe_check.css({ // on rend le champ rouge
      color: 'red',
    });
    return false;
  } else {
    $classe.css({ // si tout est bon, on le rend vert
      borderColor: 'green',
        boxShadow: '0 0 0 0.125em #00800099',
    });
    $classe_check.removeClass("fas fa-times");
    $classe_check.addClass("fas fa-check");
    $classe_check.css({ // on rend le champ rouge
      color: 'green',
    });
    return true;
  }
}

function verifLva() {
  var search = document.querySelector('#LVA');
  var results = document.querySelector('#datalist_lva');
  var templateContent = document.querySelector('#template_lva').content;
  search.addEventListener('keyup', function handler(event) {
    while (results.children.length) results.removeChild(results.firstChild);
    var inputVal = new RegExp(search.value.trim(), 'i');
    var clonedOptions = templateContent.cloneNode(true);
    var set = Array.prototype.reduce.call(clonedOptions.children, function searchFilter(frag, el) {
      if (inputVal.test(el.textContent) && frag.children.length < 5) frag.appendChild(el);
      return frag;
    }, document.createDocumentFragment());
    results.appendChild(set);
  });
  var lang = ["Allemand", "Allemand Euro", "Anglais", "Anglais Euro", "Arabe", "Basque", "Catalan", "Chinois", "Créole", "Italien", "Italien Euro", "Espagnol", "Espagnol Euro", "Hébreu", "Kanak", "Portugais", "Portugais Euro", "Russe"];
  if (lang.indexOf($lva.val()) === -1 || $lva.val() == $lvb.val()) {
    $lva.css({ // on rend le champ rouge
      borderColor: 'red',
        boxShadow: '0 0 0 0.125em #ff000099',
    });
    $lva_check.removeClass("fas fa-check");
    $lva_check.addClass("fas fa-times");
    $lva_check.css({ // on rend le champ rouge
      color: 'red',
    });
    return false;
  } else {
    $lva.css({ // si tout est bon, on le rend vert
      borderColor: 'green',
        boxShadow: '0 0 0 0.125em #00800099',
    });
    $lva_check.removeClass("fas fa-times");
    $lva_check.addClass("fas fa-check");
    $lva_check.css({ // on rend le champ rouge
      color: 'green',
    });
    $('#lvaValue').val('lv1'+langValue[$lva.val()]);
    return true;
  }
}

function verifLvb() {
  var search = document.querySelector('#LVB');
  var results = document.querySelector('#datalist_lvb');
  var templateContent = document.querySelector('#template_lvb').content;
  search.addEventListener('keyup', function handler(event) {
    while (results.children.length) results.removeChild(results.firstChild);
    var inputVal = new RegExp(search.value.trim(), 'i');
    var clonedOptions = templateContent.cloneNode(true);
    var set = Array.prototype.reduce.call(clonedOptions.children, function searchFilter(frag, el) {
      if (inputVal.test(el.textContent) && frag.children.length < 5) frag.appendChild(el);
      return frag;
    }, document.createDocumentFragment());
    results.appendChild(set);
  });
  var lang = ["Allemand", "Anglais", "Arabe", "Basque", "Catalan", "Chinois", "Créole", "Espagnol", "Hébreu", "Kanak", "Portugais", "Russe"];
  if (lang.indexOf($lvb.val()) === -1 || $lva.val() == $lvb.val()) {
    $lvb.css({ // on rend le champ rouge
      borderColor: 'red',
        boxShadow: '0 0 0 0.125em #ff000099',
    });
    $lvb_check.removeClass("fas fa-check");
    $lvb_check.addClass("fas fa-times");
    $lvb_check.css({ // on rend le champ rouge
      color: 'red',
    });
    return false;
  } else {
    $lvb.css({ // si tout est bon, on le rend vert
      borderColor: 'green',
        boxShadow: '0 0 0 0.125em #00800099',
    });
    $lvb_check.removeClass("fas fa-times");
    $lvb_check.addClass("fas fa-check");
    $lvb_check.css({ // on rend le champ rouge
      color: 'green',
    });
    $('#lvbValue').val('lv2'+langValue[$lvb.val()]);
    return true;
  }
}


$form.on('submit', function(e) {
  if (verifPhone() && verifBirthday() && verifClasse() && verifSchool(false) && verifLva() && verifLvb()) {
    return true;
  } else {
    $erreur.css({
      display: 'block',
    });
    return false;
  }
});
});
