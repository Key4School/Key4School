function input(type){
  if($('#'+ type)!==undefined){
    var contenu= $('#'+ type).html(); // renvoie le texte contenu à l'intérieur du paragraphe
    if (!contenu.includes('Non-renseigné')){
      $('#content' + type).html('<input onfocus="this.select();" onclick="this.select();" class="input" name="'+type+'" id="input'+type+'" type="text" value="'+ contenu + '"/>'); // remplace le code HTML actuel par celui-ci
    }else{
      $('#content' + type).html('<input onfocus="this.select();" onclick="this.select();" class="input" name="'+type+'" id="input'+type+'" type="text" placeholder="Non-renseigné"/>'); // remplace le code HTML actuel par celui-ci
    }
  }
}

function updateImgOpen() {
  $("#replaceImg").addClass("is-active");
}

function updateImgClose() {
  $("#replaceImg").removeClass("is-active");
}

function signalisation(){
  selectionSign = document.getElementById("sign").className
  if (selectionSign == "far fa-flag") {
    signalisationOpen();


  }
  if (selectionSign == "fas fa-flag"){
    designalisationOpen();
  }
}

function signalisationOpen() {
  $("#signalisation").addClass("is-active");
}

function signalisationClose() {
  $("#signalisation").removeClass("is-active");
}

function signaler(e) {
  e.preventDefault();
  var donnees = $('#signalement').serialize();
  $.ajax({
    url: '/signPostProfil/', // on donne l'URL du fichier de traitement
    type: "POST", // la requête est de type POST
    data: donnees, // et on envoie nos données
    success: function(response) {
      $('#signalement').trigger("reset");
      signalisationClose();
      document.getElementById("sign").className = "fas fa-flag";
    },
  });
}
