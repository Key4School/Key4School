function inputpseudo(){
  if($('#pseudo')!==undefined){
    var pseudo= $('#pseudo').html(); // renvoie le texte contenu à l'intérieur du paragraphe
    $('#contentPseudo').html('<input class="input" id="inputPseudo" type="text" value="'+ pseudo + '"/>'); // remplace le code HTML actuel par celui-ci
  }

}
function inputemail(){
  if($('#email')!==undefined){
    var email= $('#email').html(); // renvoie le texte contenu à l'intérieur du paragraphe
    $('#contentEmail').html('<input class="input" id="inputEmail" type="email" value="' + email + '"/>'); // remplace le code HTML actuel par celui-ci
  }
}
function inputinstagram(){
  if($('#instagram')!==undefined){
    var instagram= $('#instagram').html(); // renvoie le texte contenu à l'intérieur du paragraphe
    $('#contentInstagram').html('<input class="input" id="inputInstagram" type="text" value="' + instagram + '"/>'); // remplace le code HTML actuel par celui-ci
  }
}
function inputsnapchat(){
  if($('#snapchat')!==undefined){
    var snapchat= $('#snapchat').html(); // renvoie le texte contenu à l'intérieur du paragraphe
    $('#contentSnapchat').html('<input class="input" id="inputSnapchat" type="text" value="' + snapchat + '"/>'); // remplace le code HTML actuel par celui-ci
  }
}
function inputphone(){
  if($('#phone')!==undefined){
    var phone= $('#phone').html(); // renvoie le texte contenu à l'intérieur du paragraphe
    $('#contentPhone').html('<input class="input" id="inputPhone" type="text" value="' + phone + '"/>'); // remplace le code HTML actuel par celui-ci
  }
}
function inputinteret(){
  if($('#interet')!==undefined){
    var interet= $('#interet').html(); // renvoie le texte contenu à l'intérieur du paragraphe
    $('#contentInteret').html('<input class="input" id="Interet" type="text" value="' + interet + '"/>'); // remplace le code HTML actuel par celui-ci
  }
}
function inputlv(){
  if($('#lv')!==undefined){
    var lv= $('#lv').html(); // renvoie le texte contenu à l'intérieur du paragraphe
    $('#contentLv').html('<input class="input" id="Lv" type="text" value="' + lv + '"/>'); // remplace le code HTML actuel par celui-ci
  }
}