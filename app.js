const {app, BrowserWindow} = require('electron')
const url = require("url");
const path = require("path");
const fs = require("fs");

let mainWindow

const createWindow =  () => {
    mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
        nodeIntegration: true
    }
    })

    mainWindow.loadURL(
    url.format({
        pathname: path.join(__dirname, `/HomoepathyCase/index.html`),
        protocol: "file:",
        slashes: true
    })
    );
    // Open the DevTools.
    mainWindow.webContents.openDevTools()

    mainWindow.on('closed', function () {
    mainWindow = null
    })
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit()
})

app.on('activate', () => {
    if (mainWindow === null) createWindow()
})