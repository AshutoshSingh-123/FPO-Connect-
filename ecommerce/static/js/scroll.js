$(document).ready(function () {

 $(".scroll").mouseenter(function () {
  var id = $(this).attr('id');
  $('a').removeClass('active');
  $("[href=#" + id + "]").addClass('active');
 });

});
