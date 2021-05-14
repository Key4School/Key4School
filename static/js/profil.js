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
