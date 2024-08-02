const { app, BrowserWindow } = require('electron')
const path = require('node:path')
const { exec } = require('child_process')

function createWindow () {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true,
    }
  })

  mainWindow.maximize()

  // Load the index.html of the app.
  mainWindow.loadFile('pages/landing.html')

  // Open the DevTools.
  mainWindow.webContents.openDevTools()

  // Start the Python server
  const pyProcess = exec('python /Users/qiwen/Downloads/kidrone/electron/engine/server.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`Error starting Python server: ${error.message}`)
      return
    }

    if (stderr) {
      console.error(`Python server stderr: ${stderr}`)
      return
    }

    console.log(`Python server stdout: ${stdout}`)
  })

  // Ensure Python process is terminated when Electron app is closed
  mainWindow.on('closed', () => {
    pyProcess.kill()
  })
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
app.whenReady().then(() => {
  createWindow()

  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
