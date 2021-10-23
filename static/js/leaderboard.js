$(document).ready(function() {
  $('#france').click(function() {
    $('#france').addClass('is-active');
    $('#depart').removeClass('is-active');
    $('#lycee').removeClass('is-active');
  });
  $('#depart').click(function() {
    $('#depart').addClass('is-active');
    $('#france').removeClass('is-active');
    $('#lycee').removeClass('is-active');
  });
  $('#lycee').click(function() {
    $('#lycee').addClass('is-active');
    $('#france').removeClass('is-active');
    $('#depart').removeClass('is-active');
  });
});
