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
