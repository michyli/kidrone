const dispDiam = document.getElementById('dispersionDiameter');
const dispVelo = document.getElementById('dispersionVelocity');
const nondispVelo = document.getElementById('nondispersionVelocity');
const accel = document.getElementById('acceleration');
const minCover = document.getElementById('minimumCoverage');
const windDir = document.getElementById('windDirection');
const windVelo = document.getElementById('windVelocity');
const seedType = document.getElementById('seedSelection')
const saveSettingsBtn = document.getElementById('saveSettingsBtn')

const arrow = document.querySelector('.windIcon .arrow');

var settingsValues = new Map([
    ["dispersionDiameter", undefined],
    ["dispersionVelocity", undefined],
    ["nondispersionVelocity", undefined],
    ["acceleration", undefined],
    ["minimumCoverage", undefined],
    ["windDirection", undefined],
    ["windVelocity", undefined]
]);

function goBack() {
    //TODO: This need to be done without using window.history.back() because we are not redirecting URL.
    //Need to find a way to track the previous page (a variable of the ID of the previous active page need to be stored, 
    //meaning we need to keep track of the current and the last active pages' ID)
    console.log("Go back to the previous page")
}

function addSeed() {
    console.log("seed Added")
}

function storeSettingsValues() {
    for (const key of settingsValues.keys()) {
        settingsValues.set(key, document.getElementById(key).value);
    };
    const settingsValuesArray = Array.from(settingsValues.entries());
    localStorage.setItem('settingsValues', JSON.stringify(settingsValuesArray));
};

export function displaySettingsValues(subTabId) {
    for (const key of settingsValues.keys()) {
        document.querySelector(`#${subTabId} #${key}`).value = settingsValues.get(key);
    };
}

function saveSetting() {
    //Save the values in map
    storeSettingsValues();
    displaySettingsValues("settingProjectF1");

    // Save the setting's HTML structure to local storage
    localStorage.setItem('settingsHTML', document.getElementById('settingProjectF1').innerHTML);
    
    console.log("Settings saved");
}

windDir.addEventListener("change", function() {

    var angle = windDir.value
    arrow.style.transform = `rotate(${angle}deg)`;
}, false)

// Save the default setting values to local system (will last even if app closes), only if not already saved
if (localStorage.getItem('settingsValues') == null) {
    storeSettingsValues();
}
else {
    settingsValues = JSON.parse(localStorage.getItem('settingsValues'));
    settingsValues = new Map(settingsValues);
    displaySettingsValues("settingProjectF1");
}

//Observe when we switch to settings subtab, to counteract values being saved without clicking the save button
const observer = new MutationObserver((mutationsList, observer) => {
    for (const mutation of mutationsList) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
            // Get the updated class attribute value
            const newClassValue = mutation.target.getAttribute('class');
            // Check if 'active' is in the new class list
            if (newClassValue.includes('active')) {
                displaySettingsValues("settingProjectF1");
            };
        };
    };
});
const observerOptions = {
    attributes: true,
    attributeFilter: ['class'],
};
observer.observe(document.getElementById("settingProjectF1"), observerOptions)

saveSettingsBtn.addEventListener("click", saveSetting);

