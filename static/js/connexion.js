var num = 0;
var numMax = 4;
var img = ['Entraide.gif', 'everywhere.gif', "Une messagerie instantanée.gif", 'LeaderBoard.gif', 'sombreclaire.gif'];

function photo() {
  $("#img_connexion").attr('src', '../static/image/connexion/' + img[num]);
  num += 1;
  if (num == img.length) {
    num = 0
  }
}
setInterval(photo, 10000);
