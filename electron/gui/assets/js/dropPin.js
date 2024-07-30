import { switchSubTab } from "./landing.js";

const dropPinButton = document.getElementById("dropPinButton");
dropPinButton.addEventListener("click", () => {
    console.log("click")
    switchSubTab("dropPinF1");
});