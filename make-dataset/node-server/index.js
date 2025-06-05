const express = require('express');
const axios = require('axios');
const app = express();
const PORT = 3000;

app.use(express.json());

app.post('/api/state', async (req, res) => {
  const { state, timestamp } = req.body;
  console.log(`接收到状态：${state}，时间戳：${timestamp}`);

  // 转发事件到 Python 程序
  try {
    await axios.post('http://localhost:5000/event', { state, timestamp });
    res.status(200).send('状态已记录并转发');
  } catch (error) {
    console.error('转发到 Python 程序时出错:', error);
    res.status(500).send('服务器错误');
  }
});

app.listen(PORT, () => {
  console.log(`服务器正在运行，监听端口 ${PORT}`);
});
