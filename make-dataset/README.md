1. 安装依赖：

# 进入 Node 后端目录并安装依赖
cd resource-monitor-project/node-server
npm init -y
npm install express axios

# 进入 Python 采集目录并安装依赖
cd ../python-monitor
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install flask psutil
pip freeze > requirements.txt

---

2. 启动步骤：

# 1️⃣ 启动 Python 采集端
cd resource-monitor-project/python-monitor
python monitor.py

# 2️⃣ 启动 Node.js 后端
cd ../node-server
node index.js

# 3️⃣ 打开前端页面
打开浏览器，访问 frontend/index.html（可以直接拖进浏览器）

---

3. 功能说明：
- 默认每 20 秒采集一次系统资源数据
- 当用户在页面点击按钮时：
  - Node.js 接收按钮事件，并通知 Python
  - Python 将采样频率提高到 1 秒
  - 持续 1 分钟后自动恢复为 20 秒
- 所有采集结果写入 `resource_usage.csv`

如需部署为网站，可使用 Nginx、Vite、或任何静态服务器工具托管 frontend 目录



pip install pyinstaller
pyinstaller --noconsole --onefile your_flask_app.py
npm install electron-builder --save-dev
npx electron-builder