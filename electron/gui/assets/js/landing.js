const burger = document.querySelector(".burgerMenu");
const menu = document.querySelector(".menu");
const titles = document.querySelectorAll(".menu div");

const newProject = document.getElementById("new");
const browseProject = document.getElementById("browse");
const loadProject = document.getElementById("load");
const settingProject = document.getElementById("setting");
const newProjectTab = document.getElementById("newProject");
const browseProjectTab = document.getElementById("browseProject");
const loadProjectTab = document.getElementById("loadProject");
const settingProjectTab = document.getElementById("settingProject");

menu.style.height = `${menu.scrollHeight + 20}px`;

/* Burger & Menu Control */
burger.addEventListener("click", function() {
  burger.classList.toggle("active")
  if (burger.classList.contains("active")) {
    menu.style.height = `${menu.scrollHeight + 20}px`;
  } else {
    menu.style.height = '0px';
  }
})

titles.forEach((title) => {
  title.addEventListener("click", function() {
    burger.classList.remove("active")
    menu.style.height = '0px';
  })
})

/* Switch Tabs logic */
newProject.addEventListener("click", function() {
  newProjectTab.classList.add("active");
  browseProjectTab.classList.remove("active");
  loadProjectTab.classList.remove("active");
  settingProjectTab.classList.remove("active");
})
browseProject.addEventListener("click", function() {
  newProjectTab.classList.remove("active");
  browseProjectTab.classList.add("active");
  loadProjectTab.classList.remove("active");
  settingProjectTab.classList.remove("active");
})
loadProject.addEventListener("click", function() {
  newProjectTab.classList.remove("active");
  browseProjectTab.classList.remove("active");
  loadProjectTab.classList.add("active");
  settingProjectTab.classList.remove("active");
})
settingProject.addEventListener("click", function() {
  newProjectTab.classList.remove("active");
  browseProjectTab.classList.remove("active");
  loadProjectTab.classList.remove("active");
  settingProjectTab.classList.add("active");
})