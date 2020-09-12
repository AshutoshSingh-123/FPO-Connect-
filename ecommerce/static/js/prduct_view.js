var li_links = document.querySelectorAll(".links ul li");
var view_wraps = document.querySelectorAll(".view_wrap");
var list_view = document.querySelector(".list-view");
var grid_view = document.querySelector(".grid-view");

li_links.forEach(function (link) {
 link.addEventListener("click", function () {
  li_links.forEach(function (link) {
   link.classList.remove("active");
  })

  link.classList.add("active");

  var li_view = link.getAttribute("data-view");

  view_wraps.forEach(function (view) {
   view.style.display = "none";
  })

  if (li_view == "list-view") {
   list_view.style.display = "block";
  }
  else {
   grid_view.style.display = "block";
  }
 })
})

function submit(){
 
  var a=document.getElementById("form1");
  a.submit();

  
 }
function submit1(){
 
  var b=document.getElementById("form2");
  b.submit();

  
 }
function submit2(){
 
  var a=document.getElementById("form3");
  a.submit();

  
 }
