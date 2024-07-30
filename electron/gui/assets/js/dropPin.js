import { switchSubTab } from "./landing.js";

const dropPinButton = document.getElementById("dropPinButton");
dropPinButton.addEventListener("click", () => {
    switchSubTab("dropPinF1");
});