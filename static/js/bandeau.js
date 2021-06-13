function remove(){
  if (document.getElementById('bandeauDroite').style.display == "none"){
    document.getElementById('bandeauDroite').style.display = "block";
    document.getElementById('filters').style.width = "80%";
    document.getElementById('contentPost').style.width = "80%";

  }
  else{
    document.getElementById('bandeauDroite').style.display = "none";
    document.getElementById('filters').style.width = "100%";
    document.getElementById('contentPost').style.width = "100%";
  }
}
function recherche(){
  if (document.getElementById('rechercheTel').style.display == "none"){
    document.getElementById('rechercheTel').style.display = "block";

  }
  else{
    document.getElementById('rechercheTel').style.display = "none";
  }
}
