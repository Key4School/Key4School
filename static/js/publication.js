function like(id){
  selectionlike = document.getElementById("like_"+id).className
  if (selectionlike == "far fa-thumbs-up") {
    document.getElementById("like_"+id).className = "fas fa-thumbs-up";
    document.getElementById("like_"+id).innerHTML = parseInt(document.getElementById("like_"+id).innerHTML) + 1; // on ajoute 1 au nb de likes

  }
  if (selectionlike == "fas fa-thumbs-up"){
    document.getElementById("like_"+id).className = "far fa-thumbs-up";
    document.getElementById("like_"+id).innerHTML = parseInt(document.getElementById("like_"+id).innerHTML) - 1; // on enlève 1 au nb de likes
  }

  fetch(`likePost/${id}`, {
    method: 'post',
    headers: { 
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  })
    .then(nbLikes => {
      console.log(nbLikes);
    });
}

