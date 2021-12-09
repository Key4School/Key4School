function loading(){
  var color = window.getComputedStyle(document.body).getPropertyValue('--color-theme0');
  $(".container_leaderboard").html(`
    <style>
      .loading {
        position: relative;
        margin: auto;
        margin-top: 20%;
        width: 1.5em;
        height: 1.5em;
        border-radius: 50%;
        box-shadow:
          0 -3em ` + color + `ff,
          2.25em -2.25em ` + color + `dc,
          3em 0 ` + color + `be,
          2.25em 2.25em ` + color + `a0,
          0 3em ` + color + `82,
          -2.25em 2.25em ` + color + `5f,
          -3em 0 ` + color + `3c,
          -2.25em -2.25em ` + color + `1e;
        animation: spin 1.5s linear infinite;
      }

      @keyframes spin {
        100% { transform: rotate(-360deg) }
      }
    </style>
    <div class="loading"></div>`);
}

$(document).ready(function() {
  $('#lb-france').click(function() {
    $('#lb-france').addClass('is-active');
    $('#lb-depart').removeClass('is-active');
    $('#lb-lycee').removeClass('is-active');
    $.ajax({
      type: 'GET',
      url: '/leaderboard/france/1',
      async: true,
      beforeSend: loading,
      success: function(result){
        $(".container_leaderboard").html(result);
      }
    });
  });
  $('#lb-depart').click(function() {
    $('#lb-depart').addClass('is-active');
    $('#lb-france').removeClass('is-active');
    $('#lb-lycee').removeClass('is-active');
    $.ajax({
      type: 'GET',
      url: '/leaderboard/departement/1',
      async: true,
      beforeSend: loading,
      success: function(result){
        $(".container_leaderboard").html(result);
      }
    });
  });
  $('#lb-lycee').click(function() {
    $('#lb-lycee').addClass('is-active');
    $('#lb-france').removeClass('is-active');
    $('#lb-depart').removeClass('is-active');
    $.ajax({
      type: 'GET',
      url: '/leaderboard/lycee/1',
      async: true,
      beforeSend: loading,
      success: function(result){
        $(".container_leaderboard").html(result);
      }
    });
  });
});
