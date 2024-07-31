import { switchSubTab } from "./landing.js";

const plotBlockButton = document.getElementById("plotBlockButton");
plotBlockButton.addEventListener("click", () => {
    console.log("click")
    switchSubTab("plotBlockF1");
});

