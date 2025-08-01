// preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  sendState: (state, reason, timestamp) => {
    ipcRenderer.send('state-change', { state, reason, timestamp });
  }
});