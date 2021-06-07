function remove(){
  if (document.getElementById('bandeauDroite').style.display == "none"){
    document.getElementById('bandeauDroite').style.display = "block";
    document.getElementById('filters').style.width = "80%";
  }
  else{
    document.getElementById('bandeauDroite').style.display = "none";
    document.getElementById('filters').style.width = "100%";
  }
}
