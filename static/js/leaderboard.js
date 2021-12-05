$(document).ready(function() {
  $('#lb-france').click(function() {
    $('#lb-france').addClass('is-active');
    $('#lb-depart').removeClass('is-active');
    $('#lb-lycee').removeClass('is-active');
  });
  $('#lb-depart').click(function() {
    $('#lb-depart').addClass('is-active');
    $('#lb-france').removeClass('is-active');
    $('#lb-lycee').removeClass('is-active');
  });
  $('#lb-lycee').click(function() {
    $('#lb-lycee').addClass('is-active');
    $('#lb-france').removeClass('is-active');
    $('#lb-depart').removeClass('is-active');
  });
});
