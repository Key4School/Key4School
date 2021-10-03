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
    $lvb_template = $('#template_lvb');

  var pourcent = 0;
  var boul1 = false;
  var boul2 = false;
  var boul3 = false;
  var boul4 = false;

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
    var querytemp = $school.val();
    var tab = querytemp.split(" ");
    var query = tab.join('%20');
    var response = "";
    console.log(query);
    $.ajax({
      url: 'https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-en-annuaire-education&rows=1&facet=nom_etablissement&facet=nom_commune&refine.type_etablissement=Lycée',
      dataType: 'json',
      data: {
        q: $('#school').val()
      },

      success: function(donnee) {
        console.log(donnee);
        $.map(donnee, function() {
          console.log(donnee["records"].length);
          for (let i = 0; i < donnee["records"].length; i++) {
            console.log("records i", donnee["records"][i]);
            console.log("records i", donnee["records"][i]["fields"]["nom_etablissement"]);
            console.log($('#datalist_school option[datalisted=datalisted]').val());
            $('#datalist_school').append('<option>' + donnee["records"][i]["fields"]["nom_etablissement"] + ' ' + donnee["records"][i]["fields"]["nom_commune"] + '</option>');

          }

        });
      }
    });
    // var endpoint = "https://data.education.gouv.fr/api/v1/console/datasets/1.0/search/";
    // $.ajax({
    //   type: "GET",
    //   url: endpoint,
    //   params: {
    //     "dataset": "fr-en-annuaire-education",
    //     "q": query,
    //     "facet": "nom_etablissement"
    //   },
    //   dataType: "json",
    //   success: function(result, status, xhr) {
    //     console.log(result, status, xhr);
    //     console.log(result["fields"]);
    //   }
    // });




    if ($school.val().length < 3) { // si la chaîne de caractères est inférieure à 5
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
    var lang = ["Allemand", "Anglais", "Arabe", "Basque", "Catalan", "Chinois", "Créole", "Espagnol", "Hébreu", "Kanak", "Portugais", "Russe"];
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


  //   $envoi.click(function(e) {
  //      e.preventDefault(); // on annule la fonction par défaut du bouton d'envoi
  //      // on verifie que le pseudo et l'email n'existe pas encore
  //      var json;
  //      $.ajax({
  //        url: "recupPseudoEmail.php",
  //        type: "GET",
  //        dataType: 'json',
  //        async: false,
  //        success: function(out) {
  //          json = out;
  //        }
  //      });
  //     if (!json.pseudo.includes($pseudo.val()) && !json.email.includes($email.val())) {
  //       // puis on lance la fonction de vérification sur tous les champs :
  //       if (verifPrenom() && verifPseudo() && verifNom() && verifMdp() && verifConfMdp() && verifEmail()) {
  //         $form.submit();
  //       }else {
  //         $erreur.html("Vous n'avez pas rempli correctement les champs du formulaire !");// on affiche le message d'erreur
  //       }
  //     }else{
  //         $erreur.html("Ce pseudo ou cette email est déjà utilisé !");// on affiche le message d'erreur
  //     }
  //   });
});
