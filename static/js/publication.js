function like(id){
  selectionlike = document.getElementById("like"+id).className
  if (selectionlike == "far fa-thumbs-up") {
    document.getElementById("like"+id).className = "fas fa-thumbs-up";
  }
  if (selectionlike == "fas fa-thumbs-up"){
    document.getElementById("like"+id).className = "far fa-thumbs-up";
  }
}
function dislike(id){
  selectiondislike = document.getElementById("dislike"+id).className
  if (selectiondislike == "far fa-thumbs-down"){
    document.getElementById("dislike"+id).className = "fas fa-thumbs-down";
  }
  if (selectiondislike == "fas fa-thumbs-down"){
    document.getElementById("dislike"+id).className = "far fa-thumbs-down";
  }
}
