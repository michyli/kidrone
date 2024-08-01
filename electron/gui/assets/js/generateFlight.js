import { switchSubTab } from "./landing.js";
import { displaySettingsValues } from "./setting.js";
// import { run_python_script } from "./script_linker_test.js";

const dropPinButton = document.getElementById("planFlightBtn");
dropPinButton.addEventListener("click", () => {
    switchSubTab("generateFlightF1");

    //Load the settings html, delete the save button
    const settingsHTML = localStorage.getItem('settingsHTML');
    if (settingsHTML) {
        document.getElementById('settingsViewer').innerHTML = settingsHTML;

        const button = document.querySelector('#settingsViewer #saveSettingsBtn');
        button.remove();
    }
    displaySettingsValues("generateFlightF1");

    //Make all the input boxes read only
    const container = document.getElementById('settingsViewer');
    const inputs = container.querySelectorAll('input');

    inputs.forEach(input => {
        input.readOnly = true;
    });
});

// //Generate the flight path shapefile by calling python script
// const generateFlightBtn = document.getElementById("generateFlightBtn");
// generateFlightBtn.addEventListener("click", () => {
//     var message = localStorage.getItem('settingsValues') + '\n';
//     run_python_script(message);
// })

