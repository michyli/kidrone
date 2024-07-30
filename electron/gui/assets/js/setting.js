const dispDiam = document.getElementById('dispersionDiameter');
const dispVelo = document.getElementById('dispersionVelocity');
const nondispVelo = document.getElementById('nondispersionVelocity');
const accel = document.getElementById('acceleration');
const minCover = document.getElementById('minimumCoverage');
const windDir = document.getElementById('windDirection');
const windVelo = document.getElementById('windVelocity');
const seedType = document.getElementById('seedSelection')
//add .value to the end of variable to extract the value of the input

const arrow = document.querySelector('.windIcon .arrow');

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
    console.log("Settings saved")
}

windDir.addEventListener("change", function() {
    var angle = windDir.value
    arrow.style.transform = `rotate(${angle}deg)`;
}, false)

