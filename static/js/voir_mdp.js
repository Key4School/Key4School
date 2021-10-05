function voir(id) {
  if (id==1){
    var input1 = document.getElementById("mdp");
    if (input1.type == "password"){
      input1.type = "text";
      document.getElementById("oeilid").className = "fas fa-eye-slash";
    }else{
      input1.type = "password";
      document.getElementById("oeilid").className = "fas fa-eye";
    }
  }
  if (id==2){
  var input2 = document.getElementById("confmdp");
  if (input2.type == "password"){
    input2.type = "text";
    document.getElementById("oeilid2").className = "fas fa-eye-slash";
  }else{
    input2.type = "password";
    document.getElementById("oeilid2").className = "fas fa-eye";
  }
}
}
