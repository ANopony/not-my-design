const express = require('express');
const axios = require('axios');
const cors = require('cors'); // 新增
const app = express();
const PORT = 18140;

app.use(cors()); // 新增
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
  console.log(`服务器正在运行，监听端口 ${PORT}`);
});