# Author: Nopony
# Date: 2025-06-05
# Description: This script collects system resource usage data (CPU, memory, network, and GPU) and writes it to a CSV file.

# 获取CPU\内存\网络
import psutil
# 获取GPU
import pynvml
import time
import csv

# 初始化 GPU
pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)

# 打开 CSV 文件
with open('resource_usage.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # 写入表头
    writer.writerow(['timestamp', 'cpu_usage', 'mem_used', 'bytes_sent', 'bytes_recv', 'gpu_util', 'gpu_mem_used'])

    while True:
        timestamp = time.time()
        cpu_usage = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        net_io = psutil.net_io_counters()
        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
        mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)

        writer.writerow([
            timestamp,
            cpu_usage,
            mem.used,
            net_io.bytes_sent,
            net_io.bytes_recv,
            utilization.gpu,
            mem_info.used
        ])
