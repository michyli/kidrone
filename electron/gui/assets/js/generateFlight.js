import { switchSubTab } from "./landing.js";

const dropPinButton = document.getElementById("planFlightBtn");
dropPinButton.addEventListener("click", () => {
    console.log("click")
    switchSubTab("generateFlightF1");
});