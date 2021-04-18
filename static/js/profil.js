function input(type){
  if($('#'+ type)!==undefined){
    var contenu= $('#'+ type).html(); // renvoie le texte contenu à l'intérieur du paragraphe
    $('#content' + type).html('<input onfocus="this.select();" onclick="this.select();" class="input" name="'+type+'" id="input'+type+'" type="text" value="'+ contenu + '"/>'); // remplace le code HTML actuel par celui-ci
  }
}
