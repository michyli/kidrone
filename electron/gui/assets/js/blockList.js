import { switchSubTab } from "./landing.js";

const dropPinButton = document.getElementById("saveBlockBtn");
dropPinButton.addEventListener("click", () => {
    switchSubTab("blockListF1");
});