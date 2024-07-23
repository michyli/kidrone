function run_python_test() {

    //Just checking if the button got clicked
    document.getElementById('detect').value = 'BUTTON PRESSED';
    console.log("Button Clicked");

    //Initialize pythonshell and get path to python script directory (not the path to the script itself)
    var { PythonShell } = require("python-shell");
    var path = require("path");
    console.log(path.join(__dirname, '../engine/script_linker_test.py'))

    //Set options for pyshellcd
    let options = {
        mode: 'text',
        pythonOptions: ['-u'], // get print results in real-time
        scriptPath: path.join(__dirname, '../engine')        
    };

    let pyshell = new PythonShell('script_linker_test.py', options);

    // Run the Python script with callback function everytime message is read
    pyshell.on('message', function (message) {
        console.log('Python script read from successfully');
        console.log('Results:', message); 
        document.getElementById('output').textContent = message
    });

    //Send data to python script
    pyshell.send('Testing sending data to python script')
    
    // Handle errors during the execution of the Python script
    pyshell.on('error', function (err) {
        console.error('Error occurred:', err);
    });

    // end the input stream and allow the process to exit
    pyshell.end(function (err,code,signal) {
        if (err) throw err;
        console.log('The exit code was: ' + code);
        console.log('The exit signal was: ' + signal);
        console.log('finished');
    });
}