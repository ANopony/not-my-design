import psutil

# CPU 使用率（百分比）
cpu_usage = psutil.cpu_percent(interval=1)

# 每个核心的 CPU 使用率
cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)

# 内存使用
mem = psutil.virtual_memory()
mem_total = mem.total / (1024 ** 3)  # GB
mem_used = mem.used / (1024 ** 3)    # GB
mem_percent = mem.percent            # 使用百分比

# 网络 I/O
net = psutil.net_io_counters()
bytes_sent = net.bytes_sent / (1024 ** 2)  # MB
bytes_recv = net.bytes_recv / (1024 ** 2)  # MB

print(f"CPU使用率: {cpu_usage}%")
print(f"每核CPU使用率: {cpu_per_core}")
print(f"内存: {mem_used:.2f}GB / {mem_total:.2f}GB ({mem_percent}%)")
print(f"网络发送: {bytes_sent:.2f}MB, 接收: {bytes_recv:.2f}MB")
