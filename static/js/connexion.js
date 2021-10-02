var num=0;//num ninimum
var numMax=1;//nombre d'image a faire defilé +1


function photo(){
  $("#img_connexion").attr('src','../static/image/connexion/pub'+num+'.png');
  num+=1;
  if (num==numMax){
    num=0
  }
}
setInterval(photo, 5000);
