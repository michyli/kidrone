const { spawn } = require("child_process");

function run_python_test() {

    //Just checking if the button got clicked
    document.getElementById('detect').value = 'BUTTON PRESSED';
    console.log("Button Clicked");

    //Initialize pythonshell and get path to python script directory (not the path to the script itself)
    var { PythonShell } = require("python-shell");
    var path = require("path");
    // Check if running in production, run these commands in terminal based on version
    //TODO: process.env.NODE_ENV isn't actually set to anything, it's null be default, so this only works by setting it mannually into dev mode
    ///[$env:NODE_ENV="development"; npm start] (Windows)
    ///[NODE_ENV=development npm start] (MacOS/Linux)
    console.log(process.env.NODE_ENV)
    if (process.env.NODE_ENV === 'development') {
        ScriptPath = path.join(__dirname, '../engine');
        ScriptName = 'script_linker_test.py'
    } else {
        console.log('In production');
        // ScriptPath = process.resourcesPath;
        ScriptPath = path.join(__dirname, '../script_linker_test.exe');
        // ScriptPath = path.join(__dirname, '../engine/dist/script_linker_test.exe');
        ScriptName = 'script_linker_test.exe';
    }
    
    console.log('ScriptPath: ', ScriptPath);
    console.log('ScriptName: ', ScriptName);

    //Set options for pyshellcd
    let options = {
        mode: 'text',
        pythonOptions: ['-u'], // get print results in real-time
        scriptPath: ScriptPath
    };

    let pyshell;
    if (ScriptName.endsWith('.py')) {
        pyshell = new PythonShell(ScriptName, options); // For Python scripts
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

    } else if (ScriptName.endsWith('.exe')) {
        const startTime = performance.now();
        // Execute the .exe file directly
        // Spawn the executable
        const executable = spawn(ScriptPath, [], { cwd: path.dirname(ScriptPath) });

        // Send data to the executable
        executable.stdin.write('Testing sending data to python script\n');
        executable.stdin.end(); // Close stdin to signal that no more data will be sent

        executable.stdout.on('data', function (data) {
            console.log('Python script read from successfully');
            console.log('Results:', data.toString());
            document.getElementById('output').textContent = data.toString();
        });

        executable.stderr.on('data', function (data) {
            console.error('Error occurred:', data.toString());
        });

        executable.on('close', function (code) {
            console.log('The exit code was: ' + code);
            const endTime = performance.now();
            const timeTaken = endTime - startTime;
            console.log(`finished in ${timeTaken.toFixed(2)} milliseconds`);
        });

        return;
    }

    
}