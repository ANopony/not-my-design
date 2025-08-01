from flask import Flask, request
import threading
import time
import psutil
import pynvml
import csv
import clr
import os
import logging

# 日志目录和文件
log_dir = os.path.join(os.path.expanduser("~"), "monitor")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "monitor.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

# dll 在用户目录下
dll_path = os.path.join(os.path.expanduser("~"), "monitor", "LibreHardwareMonitorLib.dll")
clr.AddReference(dll_path)
from LibreHardwareMonitor.Hardware import Computer

# csv 在用户目录下
csv_path = os.path.join(os.path.expanduser("~"), "monitor", "resource_usage_0721.csv")

def get_gpu_info():
    computer = Computer()
    computer.IsGpuEnabled = True
    computer.Open()
    gpu_util = None
    gpu_mem_used = None
    for hardware in computer.Hardware:
        if hardware.HardwareType.ToString() == "GpuAmd" or hardware.HardwareType.ToString() == "GpuNvidia" or hardware.HardwareType.ToString() == "GpuIntel":
            hardware.Update()
            for sensor in hardware.Sensors:
                if sensor.SensorType.ToString() == "Load" and "Core" in sensor.Name:
                    gpu_util = sensor.Value
                if sensor.SensorType.ToString() == "SmallData" and "Memory Used" in sensor.Name:
                    gpu_mem_used = sensor.Value
    return gpu_util, gpu_mem_used


app = Flask(__name__)

# 默认采样间隔为20秒
sampling_interval = 2
sampling_lock = threading.Lock()

event_log = []

def collect_resource_data():
    while True:
        with sampling_lock:
            interval = sampling_interval
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        net_io = psutil.net_io_counters()
        gpu_util, gpu_mem_used = get_gpu_info()

        # 采集线程只写入常规数据，不写state/reason
        with open(csv_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                timestamp,
                cpu_usage,
                memory.percent,
                net_io.bytes_sent,
                net_io.bytes_recv,
                gpu_util,
                gpu_mem_used,
                '',    # state
                ''     # reason
            ])
        time.sleep(interval)

@app.route('/event', methods=['POST'])
def handle_event():
    global sampling_interval
    data = request.get_json()
    state = data.get('state')
    timestamp = data.get('timestamp')
    reason = data.get('reason', '')
    event_log.append((timestamp, state, reason))
    logging.info(f"收到事件: state={state}, reason={reason}, timestamp={timestamp}")

    # 立即采集一次资源并写入csv
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    net_io = psutil.net_io_counters()
    gpu_util, gpu_mem_used = get_gpu_info()
    logging.info(f"事件采集: cpu={cpu_usage}, mem={memory.percent}, net=({net_io.bytes_sent},{net_io.bytes_recv}), gpu=({gpu_util},{gpu_mem_used}), state={state}, reason={reason}")

    with open(csv_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            cpu_usage,
            memory.percent,
            net_io.bytes_sent,
            net_io.bytes_recv,
            gpu_util,
            gpu_mem_used,
            state,
            reason
        ])

    if state == 1:
        with sampling_lock:
            sampling_interval = 2
        threading.Timer(60, reset_sampling_interval).start()
    return '事件已处理', 200


def reset_sampling_interval():
    global sampling_interval
    with sampling_lock:
        sampling_interval = 2
    print("采样间隔已重置为20秒")

if __name__ == '__main__':
    # 写入CSV表头
    # 判断文件是否存在，已存在则续写
    if not os.path.exists(csv_path):
        # 如果文件不存在，则创建并写入表头
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['timestamp', 'cpu_usage', 'memory_percent', 'bytes_sent', 'bytes_recv', 'gpu_utilization', 'gpu_memory_used', 'state', 'reason'])
    else:
        print("文件已存在，续写数据")
        pass
    
    # 启动资源采集线程
    
    threading.Thread(target=collect_resource_data, daemon=True).start()
    # 启动 Flask 服务器
    app.run(port=943)
