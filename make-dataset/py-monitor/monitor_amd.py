from flask import Flask, request
import threading
import time
import psutil
import pynvml
import csv


import clr
import os

dll_path = r"C:\File\PycharmProjects\not-my-design\LibreHardwareMonitorLib.dll"
clr.AddReference(dll_path)
from LibreHardwareMonitor.Hardware import Computer

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
sampling_interval = 20
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
        with open('resource_usage.csv', 'a', newline='') as csvfile:
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
    print("event_log:", event_log)

    # 立即采集一次资源并写入csv
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    net_io = psutil.net_io_counters()
    gpu_util, gpu_mem_used = get_gpu_info()
    with open('resource_usage.csv', 'a', newline='') as csvfile:
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
            sampling_interval = 1
        threading.Timer(60, reset_sampling_interval).start()
    return '事件已处理', 200


def reset_sampling_interval():
    global sampling_interval
    with sampling_lock:
        sampling_interval = 20
    print("采样间隔已重置为20秒")

if __name__ == '__main__':
    # 写入CSV表头
    with open('resource_usage.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['timestamp', 'cpu_usage', 'memory_percent', 'bytes_sent', 'bytes_recv', 'gpu_utilization', 'gpu_memory_used', 'state', 'reason'])
    # 启动资源采集线程
    threading.Thread(target=collect_resource_data, daemon=True).start()
    # 启动 Flask 服务器
    app.run(port=943)
