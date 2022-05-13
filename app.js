const {app, BrowserWindow} = require('electron')
const url = require("url");
const path = require("path");

let mainWindow;

const args = process.argv.slice(1),
      serve = args.some(val => val === '--serve');

const createWindow =  () => {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        icon: (serve) ? path.join(__dirname, `/src/assets/logo.png`) : path.join(__dirname, `/HomoepathyCase/assets/logo.png`),
        webPreferences: {
            nodeIntegration: true,
            allowRunningInsecureContent: (serve) ? true : false,
        }
    })

    if (serve) {
        const debug = require('electron-debug');
        debug();

        require('electron-reloader')(module);
        mainWindow.loadURL('http://localhost:4200');
    } else {
        mainWindow.loadURL(
            url.format({
                pathname: path.join(__dirname, `/HomoepathyCase/index.html`),
                protocol: 'file:',
                slashes: true
          })
        );
    }

    // Open the DevTools.
    mainWindow.webContents.openDevTools()

    mainWindow.on('closed', function () {
        mainWindow = null;
    })
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit()
})

app.on('activate', () => {
    if (mainWindow === null) createWindow()
})