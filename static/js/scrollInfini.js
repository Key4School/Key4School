$(window).data('ajaxready', true);

if (document.location.pathname == '/rechercheUser/') {
  // si c pour les user
  var url = '/moreUser/';
  var $content = $('#users');
} else {
  // si c pour les publications
  var url = '/morePost/';
  var $content = $('#publis');
}

var lastPost = 10;

if (search === undefined) {
  var search = "";
}

$(window).scroll(function() {
  if ($(window).data('ajaxready') == false) return;

  if (($(window).scrollTop() + $(window).height()) + 300 >= $(document).height()) {

    $(window).data('ajaxready', false);
    $.ajax({
      url: url, // on donne l'URL du fichier de traitement
      type: "POST", // la requête est de type POST
      data: {
        'lastPost': lastPost,
        'search': search
      }, // et on envoie nos données
      success: function(json) {
        lastPost = json.lastPost;
        if (json.html != '') {
          $content.append(json.html);
          $(window).data('ajaxready', true);
        } else {
          if (search != '') {
            $content.append("<p>Aucun autre résultat</p>");
          } else {
            $content.append("<p>Aucune nouvelle demande d'aide</p>");
          }
        }
      },
    });
  }
});
