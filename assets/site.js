document.addEventListener("DOMContentLoaded", function () {
  var btn = document.querySelector(".site-menu-btn");
  var menu = document.querySelector(".site-mobile-menu");
  if (btn && menu) {
    btn.addEventListener("click", function () {
      var open = menu.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }
});
