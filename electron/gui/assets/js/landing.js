const burger = document.querySelector(".burgerMenu");
const menu = document.querySelector(".menu");
const titles = document.querySelectorAll(".menu div");

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

/* Tab Routing */
const mainTabRef = {
  "new": ["newProject", "newProjectF1"],
  "browse": ["browseProject", "browseProjectF1"],
  "load": ["loadProject", "loadProjectF1"],
  "setting": ["settingProject", "settingProjectF1"],
  "locateButton": ["afterLocateBtn", "afterLocateBtnF1"],
}; // Add ID of tab in the respective bracket based on sequence

/* Main Tabs Routing */
const mainTabs = Object.keys(mainTabRef);
const mainTabsDependency = Object.values(mainTabRef);

mainTabs.forEach((tab) => {
  var tabRef = document.getElementById(tab);
  var mainContentsRef = mainTabRef[tab].map((ref) => document.getElementById(ref))

  tabRef.addEventListener("click", function() {
    const activeItems = document.querySelectorAll(".active");
    activeItems.forEach((el) => {
      el.classList.remove('active');
    });
    mainContentsRef.forEach((cont) => {
      cont.classList.add("active")
    });
  })
});

export function switchSubTab(nextSubTabID) {
  const activeSubTabs = document.querySelectorAll(".subTab.active");
  activeSubTabs.forEach((el) => {
    el.classList.remove('active');
  })

  document.getElementById(nextSubTabID).classList.add('active');

};

