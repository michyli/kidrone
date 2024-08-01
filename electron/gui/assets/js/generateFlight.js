import { switchSubTab } from "./landing.js";

const dropPinButton = document.getElementById("planFlightBtn");
dropPinButton.addEventListener("click", () => {
    switchSubTab("generateFlightF1");
});

document.getElementById("testing thing").addEventListener("click", () => {
    console.log(localStorage.getItem("settingsHTML"));
    console.log(localStorage.getItem('settingsValues'))
});