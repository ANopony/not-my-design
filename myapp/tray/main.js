const { app, BrowserWindow, Tray, Menu } = require('electron');
const path = require('path');
const os = require("os");
const { spawn } = require('child_process');
const { startNodeServer } = require('./index.js')

let tray = null;
let window = null;
let currentState = 0;

function createWindow() {
  window = new BrowserWindow({
    width: 300,
    height: 150,
    frame: false,
    resizable: false,
    alwaysOnTop: true,
    skipTaskbar: true,
    show: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    }
  });

  window.loadFile('index.html');
  window.on('blur', () => window.hide()); // 点击外部自动隐藏
}

app.whenReady().then(() => {

  // 在用户目录下
  const pyExePath = path.join(os.homedir(),'monitor','monitor_amd.exe');
  const pythonBackend = spawn(pyExePath);

  pythonBackend.stdout.on('data', data => {
    console.log(`Python 后端: ${data}`);
  });

  pythonBackend.stderr.on('data', data => {
    console.error(`Python 错误: ${data}`);
  });

  createWindow();
  startNodeServer();

  

  tray = new Tray(path.join(__dirname, 'icon.jpg'));
  const contextMenu = Menu.buildFromTemplate([
    { label: '退出', click: () => app.quit() }
  ]);
  tray.setToolTip('资源切换助手');
  tray.setContextMenu(contextMenu);

  tray.on('click', () => {
    window.isVisible() ? window.hide() : window.show();
    const { x, y } = tray.getBounds();
    const { width, height } = window.getBounds();
    window.setBounds({
      x: x - width / 2,
      y: y - height - 10,
      width,
      height
    });
    window.show();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
