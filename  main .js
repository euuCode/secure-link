const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { PythonShell } = require('python-shell');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 500,
        frame: false,
        backgroundColor: '#0F1419',
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
    });

    mainWindow.loadFile('index.html');
    mainWindow.setMenu(null);

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});

ipcMain.on('create-link', (event, data) => {
    const options = {
        scriptPath: path.join(__dirname),
        args: [JSON.stringify(data)]
    };

    PythonShell.run('backend.py', options, (err, results) => {
        if (err) {
            event.reply('create-link-reply', { error: err.message });
            return;
        }
        event.reply('create-link-reply', JSON.parse(results[0]));
    });
});

ipcMain.on('generate-pdf', (event) => {
    const options = {
        scriptPath: path.join(__dirname),
        args: ['generate_pdf']
    };

    PythonShell.run('backend.py', options, (err, results) => {
        if (err) {
            event.reply('generate-pdf-reply', { error: err.message });
            return;
        }
        event.reply('generate-pdf-reply', JSON.parse(results[0]));
    });
});