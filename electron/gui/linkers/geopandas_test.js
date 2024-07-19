function run_python_test() {

    document.getElementById('detect').value = 'BUTTON PRESSED';
    console.log("Button Clicked");

    var { PythonShell } = require("python-shell");
    var path = require("path");
    console.log(path.join(__dirname, '../engine/geopandas_test.py'))

    PythonShell.run(path.join(__dirname, '../engine/geopandas_test.py'), null, function (err, results) {
        if (err) {
            console.error('Error:', err);
            document.getElementById('detect').value = 'Error running Python script';
        } else {
            console.log('Python script executed successfully');
            document.getElementById('detect').value = 'Python script executed successfully';
            // console.log('Results:', results); // Log the results of the Python script execution
        }
        console.log('THING IS DONE RUNNING')
    });
}