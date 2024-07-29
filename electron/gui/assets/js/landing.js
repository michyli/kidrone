const burger = document.querySelector(".burgerMenu");
const menu = document.querySelector(".menu");

burger.addEventListener("click", function() {
  burger.classList.toggle("active")
  if (burger.classList.contains("active")) {
    menu.style.height = `${menu.scrollHeight + 20}px`;
  } else {
    menu.style.height = '0px';
  }
})
