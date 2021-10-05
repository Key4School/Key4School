$(document).ready(function() {

  var $phone = $('#phone'),
    $phone_check = $('#phone_check'),
    $birthday = $('#birthday'),
    $birthday_check = $('#birthday_check'),
    $school = $('#school'),
    $school_check = $('#school_check'),
    $grade = $('#grade'),
    $grade_check = $('#grade_check'),
    $lva = $('#LVA'),
    $lva_check = $('#LVA_check'),
    $lva_list = $('#datalist_lva'),
    $lva_template = $('#template_lva'),
    $lvb = $('#LVB'),
    $lvb_check = $('#LVB_check'),
    $lvb_list = $('#datalist_lvb'),
    $lvb_template = $('#template_lvb'),
    $form = $('#form'),
    $erreur = $('#erreur');

    $erreur.css({ // on rend le champ rouge
      display: 'block',
    });

  $phone.keyup(function() {
    verifPhone();
  });
  $birthday.keyup(function() {
    verifBirthday();
  });
  $school.keyup(function() {
    verifSchool();
  });
  $grade.change(function() {
    verifGrade();
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

    if (!phoneReg.test(phoneVal) || phoneVal == '') {
      $phone.css({ // si tout est bon, on le rend vert
        border: '3px solid red',
      });
      $phone_check.removeClass("fas fa-check");
      $phone_check.addClass("fas fa-times");
      $phone_check.css({ // on rend le champ rouge
        color: 'red',
      });
      return false;
    } else {
      $phone.css({ // si tout est bon, on le rend vert
        border: '3px solid green',
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
        border: '3px solid red',
      });
      $birthday_check.removeClass("fas fa-check");
      $birthday_check.addClass("fas fa-times");
      $birthday_check.css({ // on rend le champ rouge
        color: 'red',
      });
      return false;
    } else {
      $birthday.css({ // si tout est bon, on le rend vert
        border: '3px solid green',
      });
      $birthday_check.removeClass("fas fa-times");
      $birthday_check.addClass("fas fa-check");
      $birthday_check.css({ // on rend le champ rouge
        color: 'green',
      });
      return true;
    }
  }


  function verifSchool() {
    var querytemp = $school.val(),
      tab = querytemp.split(" "),
      query = tab.join('%20'),
      response = "",
      lycee = [],
      lyceeFinal = [];

    $.ajax({
      url: 'https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-en-annuaire-education&facet=nom_etablissement&facet=nom_commune&refine.type_etablissement=Lycée',
      dataType: 'json',
      data: {
        q: $('#school').val()
      },
      success: function(donnee) {
        $('#datalist_school').empty();
        lycee = [];
        $.map(donnee, function() {
          for (let i = 0; i < donnee["records"].length; i++) {
            if (lycee.length <= 9) {
              lycee.push(donnee["records"][i]["fields"]["nom_etablissement"] + ' ' + donnee["records"][i]["fields"]["nom_commune"]);
            } else {}
          }
        });
        for (let j = 0; j < lycee.length; j++) {
          // $('#datalist_school').append('<option>' + lycee[j] + '</option>');
          $('#school').autocomplete({
            autoFocus: true,
            source: function(request, response){
              response(lycee);
            },
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
            return false;
          } else {
            $school.css({ // si tout est bon, on le rend vert
              border: '3px solid green',
            });
            $school_check.removeClass("fas fa-times");
            $school_check.addClass("fas fa-check");
            $school_check.css({ // on rend le champ rouge
              color: 'green',
            });
            return true;
          }


        }
      }
    });
  }

function verifGrade() {
  var gradeNone = "--Niveau--";

  var gradeVal = $grade.val();
  console.log(gradeVal);

  if (gradeVal == gradeNone) {
    $grade.css({ // on rend le champ rouge
      border: '3px solid red',
    });
    $grade_check.removeClass("fas fa-check");
    $grade_check.addClass("fas fa-times");
    $grade_check.css({ // on rend le champ rouge
      color: 'red',
    });
    return false;
  } else {
    $grade.css({ // si tout est bon, on le rend vert
      border: '3px solid green',
    });
    $grade_check.removeClass("fas fa-times");
    $grade_check.addClass("fas fa-check");
    $grade_check.css({ // on rend le champ rouge
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
  if (lang.indexOf($lva.val()) === -1) {
    $lva.css({ // on rend le champ rouge
      border: '3px solid red',
    });
    $lva_check.removeClass("fas fa-check");
    $lva_check.addClass("fas fa-times");
    $lva_check.css({ // on rend le champ rouge
      color: 'red',
    });
    return false;
  } else {
    $lva.css({ // si tout est bon, on le rend vert
      border: '3px solid green',
    });
    $lva_check.removeClass("fas fa-times");
    $lva_check.addClass("fas fa-check");
    $lva_check.css({ // on rend le champ rouge
      color: 'green',
    });
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
  if (lang.indexOf($lva.val()) === -1) {
    $lvb.css({ // on rend le champ rouge
      border: '3px solid red',
    });
    $lvb_check.removeClass("fas fa-check");
    $lvb_check.addClass("fas fa-times");
    $lvb_check.css({ // on rend le champ rouge
      color: 'red',
    });
    return false;
  } else {
    $lvb.css({ // si tout est bon, on le rend vert
      border: '3px solid green',
    });
    $lvb_check.removeClass("fas fa-times");
    $lvb_check.addClass("fas fa-check");
    $lvb_check.css({ // on rend le champ rouge
      color: 'green',
    });
    return true;
  }
}


$form.on('submit', function(e) {
  if (verifPhone() && verifBirthday() && verifGrade() && verifSchool() && verifLva() && verifLvb()) {
    $form.submit();
    return true;
  } else {
    $erreur.css({
      display: 'block',
    });
    return false;
  }
});
});
