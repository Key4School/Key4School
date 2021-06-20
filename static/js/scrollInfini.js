var lastPost = 10;

var deviceAgent = navigator.userAgent.toLowerCase();
var agentID = deviceAgent.match(/(iphone|ipod|ipad)/);
$(window).data('ajaxready', true);

if (search === undefined){
  var search = "";
}

$(window).scroll(function() {
  if ($(window).data('ajaxready') == false) return;

  if (($(window).scrollTop() + $(window).height()) + 300 >= $(document).height() ||
    agentID && ($(window).scrollTop() + $(window).height()) + 300 > $(document).height()) {

    $(window).data('ajaxready', false);
    $.ajax({
      url: '/morePost/', // on donne l'URL du fichier de traitement
      type: "POST", // la requête est de type POST
      data: {
        'lastPost': lastPost,
        'search': search
      }, // et on envoie nos données
      success: function(json) {
        lastPost = json.lastPost;
        if (json.html != '') {
          $('#publis').append(json.html);
          $(window).data('ajaxready', true);
        } else {
          $('#publis').append("<p>Aucune nouvelle demande d'aide</p>");
        }
      },
    });
  }
});
