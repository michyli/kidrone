const fileInput = document.getElementById('uploadProject');
const fileUploadText = document.getElementById('uploadText');

fileInput.addEventListener('change', function () {
  // Called when files change.
  var fileName = fileInput.files[0]['name'];
  console.log(typeof fileName);
  fileUploadText.innerHTML = `File Selected: ${fileName}`;
}, false);