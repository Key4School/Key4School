var num=0;//num ninimum
var numMax=2;//nombre d'image a faire defilé +1
var img=['Entraide.gif', 'everywhere.gif'];

function photo(){
  $("#img_connexion").attr('src','../static/image/connexion/'+img[num]);
    num+=1;
  if (num==numMax){
    num=0
  }
}
setInterval(photo, 10000);
