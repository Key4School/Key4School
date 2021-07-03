$(document).ready(function() {
  // redirection to HTTPS
  if(document.location.host === 'key4school.herokuapp.com' && document.location.protocol === 'http:')
    document.location.href = document.location.href.replace(/^http/, 'https');

  // Check for click events on the navbar burger icon
  $(".navbar-burger").click(function() {

      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      $(".navbar-burger").toggleClass("is-active");
      $(".navbar-menu").toggleClass("is-active");

  });
});
$(".navbar-item.has-dropdown").click(function(e) {
      if ($(".navbar-burger").is(':visible')) {
        $(this).toggleClass("is-active");
      }
  });
  $(".navbar-item > .navbar-link").click(function(e) {
      if ($(".navbar-burger").is(':visible')) {
        e.preventDefault();
      }
  });
  $(window).resize(function(e) {
    if (!$(".navbar-burger").is(':visible') && $(".navbar-item.has-dropdown.is-active").length) {
      $(".navbar-item.has-dropdown.is-active").removeClass('is-active');
    }
  });

  function apercuProfil(id){
    if (! window['divOpen_' + id]){
    document.getElementById("apercu2profil"+id).style.display = "block";
    window['divOpen_' + id] = true;
    }
  }

  function hideApercuProfil(id) {
    if ( window['divOpen_' + id]){
    document.getElementById("apercu2profil"+id).style.display = "none";
    window['divOpen_' + id] = false;
    }
  }
