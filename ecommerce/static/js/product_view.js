var li_links = document.querySelectorAll(".links ul li");
var view_wraps = document.querySelectorAll(".view_wrap");
var list_view = document.querySelector(".list-view");
var grid_view = document.querySelector(".grid-view");

li_links.forEach(function (link) {
  link.addEventListener("click", function () {
    li_links.forEach(function (link) {
      link.classList.remove("active");
    });

    link.classList.add("active");

    var li_view = link.getAttribute("data-view");

    view_wraps.forEach(function (view) {
      view.style.display = "none";
    });

    if (li_view == "list-view") {
      list_view.style.display = "block";
    } else {
      grid_view.style.display = "block";
    }
  });
});

// filter checkbox------------------------------------

function printChecked() {
  ch=0
  var items = document.getElementsByName("acs");
  var items1 = document.getElementsByName("acs1");
  var selectedItems = "";
  var all = document.getElementsByClassName("resultblock");
  for (var j = 0; j < all.length; j++) {
    all[j].style.display = "none";
  }

  for (var i = 0; i < items.length; i++) {
    if (items[i].type == "checkbox" && items[i].checked == true) {
      ch=ch+1
      selectedItems += items[i].value + "\n";
      var x = document.getElementsByClassName(items[i].value);
      console.log(x);
      for (var j = 0; j < x.length; j++) {
        x[j].style.display = "block";
      }
    }
  }
  if (ch == 0) {
    for (var j = 0; j < all.length; j++) {
      all[j].style.display = 'block';
    }
  }
}


function printChecked1() {
  ch=0
  var items = document.getElementsByName("acs1");
  
  var all = document.getElementsByClassName("resultblock");
  for (var j = 0; j < all.length; j++) {
    all[j].style.display = "none";
  }

  for (var i = 0; i < items.length; i++) {
    if (items[i].type == "checkbox" && items[i].checked == true) {
      ch=ch+1
      
      var x = document.getElementsByClassName(items[i].value);
    ;
      for (var j = 0; j < x.length; j++) {
        x[j].style.display = "block";
      }
    }
  }
  if (ch == 0) {
    for (var j = 0; j < all.length; j++) {
      all[j].style.display = 'block';
    }
  }
}

