// node_server/index.js
const express = require('express');
const axios = require('axios');
const cors = require('cors');

function startNodeServer() {
  const app = express();
  const PORT = 18140;

  app.use(cors());
  app.use(express.json());

  app.post('/api/state', async (req, res) => {
    const { state, timestamp, reason } = req.body;

    try {
      await axios.post('http://localhost:943/event', { state, timestamp, reason });
      res.status(200).send('已记录');
    } catch (err) {
      console.error(err);
      res.status(500).send('转发失败');
    }
  });

  app.listen(PORT, () => {
    console.log(`Node.js 服务器运行在端口 ${PORT}`);
  });
}

module.exports = { startNodeServer };
