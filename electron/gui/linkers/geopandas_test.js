function run_geo_test() {

    document.getElementById('detect').value = 'BUTTON PRESSED';
    console.log("Button Clicked");

    var { PythonShell } = require("python-shell");
    var path = require("path");

    // path.join(path, '/../../engine/geopandas_test.py')
    PythonShell.run(path.join(path, 'engine', 'geopandas_test.py'), null, function (err, results) {
        if (err) {
            console.error('Error:', err);
            document.getElementById('detect').value = 'Error running Python script';
        } else {
            console.log('Python script executed successfully');
            document.getElementById('detect').value = 'Python script executed successfully';
            console.log('Results:', results); // Log the results of the Python script execution
        }
    });
}