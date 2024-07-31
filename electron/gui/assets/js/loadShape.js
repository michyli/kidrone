import { switchSubTab } from "./landing.js";

const dropPinButton = document.getElementById("loadShapeButton");
dropPinButton.addEventListener("click", () => {
  console.log("load shape clicked");
  switchSubTab("loadShapeF1");
});

const fileInput = document.getElementById('uploadShape');
const fileUploadText = document.getElementById('uploadShapeText');

fileInput.addEventListener('change', function () {
  // Called when files change.
  var fileName = fileInput.files[0]['name'];
  console.log(typeof fileName);
  fileUploadText.innerHTML = `File Selected: ${fileName}`;
}, false);