const dispDiam = document.getElementById('dispersionDiameter');
const dispVelo = document.getElementById('dispersionVelocity');
const nondispVelo = document.getElementById('nondispersionVelocity');
const accel = document.getElementById('acceleration');
const minCover = document.getElementById('minimumCoverage');
const windDir = document.getElementById('windDirection');
const windVelo = document.getElementById('windVelocity');
const seedType = document.getElementById('seedSelection')
const saveSettingsBtn = document.getElementById('saveSettingsBtn')
//add .value to the end of variable to extract the value of the input

const arrow = document.querySelector('.windIcon .arrow');

// Save the default setting values to local system (will last even if app closes)
const settingsValues = new Map();
settingsValues["dispersionDiameter"] = document.getElementById("dispersionDiameter").value;
settingsValues["dispersionVelocity"] = document.getElementById("dispersionVelocity").value;
settingsValues["nondispersionVelocity"] = document.getElementById("nondispersionVelocity").value;
settingsValues["acceleration"] = document.getElementById("acceleration").value;
settingsValues["minimumCoverage"] = document.getElementById("minimumCoverage").value;
settingsValues["windDirection"] = document.getElementById("windDirection").value;
settingsValues["windVelocity"] = document.getElementById("windVelocity").value;
localStorage.setItem('settingsValues', settingsValues);

function goBack() {
    //TODO: This need to be done without using window.history.back() because we are not redirecting URL.
    //Need to find a way to track the previous page (a variable of the ID of the previous active page need to be stored, 
    //meaning we need to keep track of the current and the last active pages' ID)
    console.log("Go back to the previous page")
}

function addSeed() {
    console.log("seed Added")
}

function saveSetting() {
    //TODO: Need to store the current values somewhere to use.
    // Save the setting's HTML structure to local storage
    localStorage.setItem('settingsHTML', document.getElementById('settingProjectF1').innerHTML);
    
    // Save the changed setting values to local system (will last even if app closes)
    settingsValues["dispersionDiameter"] = document.getElementById("dispersionDiameter").value;
    settingsValues["dispersionVelocity"] = document.getElementById("dispersionVelocity").value;
    settingsValues["nondispersionVelocity"] = document.getElementById("nondispersionVelocity").value;
    settingsValues["acceleration"] = document.getElementById("acceleration").value;
    settingsValues["minimumCoverage"] = document.getElementById("minimumCoverage").value;
    settingsValues["windDirection"] = document.getElementById("windDirection").value;
    settingsValues["windVelocity"] = document.getElementById("windVelocity").value;

    localStorage.setItem('settingsValues', JSON.stringify(settingsValues));

    console.log("Settings saved");
}

windDir.addEventListener("change", function() {

    var angle = windDir.value
    arrow.style.transform = `rotate(${angle}deg)`;
}, false)

saveSettingsBtn.addEventListener("click", saveSetting);

