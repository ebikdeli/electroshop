///navbar//////
$("#header").prepend('<div id="menu-icon"><span class="first"></span><span class="second"></span><span class="third"></span></div>');

$("#menu-icon").on("click", function () {
  $("nav").slideToggle();
  $(this).toggleClass("active");
});
///navbar//////
///card//////
$(document).ready(function () {
  $(".card")
    .delay(1800)
    .queue(function (next) {
      $(this).removeClass("hover");
      $("a.hover").removeClass("hover");
      next();
    });
});
///card//////
///////////login//////////
const signInBtn = document.getElementById("signIn");
const signUpBtn = document.getElementById("signUp");
const fistForm = document.getElementById("form1");
const secondForm = document.getElementById("form2");
const container = document.querySelector(".container");

signInBtn.addEventListener("click", () => {
  container.classList.remove("right-panel-active");
});

signUpBtn.addEventListener("click", () => {
  container.classList.add("right-panel-active");
});

fistForm.addEventListener("submit", (e) => e.preventDefault());
secondForm.addEventListener("submit", (e) => e.preventDefault());
///////////login//////////

/* ///////////details page///////// */

/* ///////////details page///////// */
