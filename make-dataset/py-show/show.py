import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../py-monitor/resource_usage.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

plt.figure(figsize=(12, 6))
plt.plot(df['timestamp'], df['cpu_usage'], label='CPU Usage (%)')
plt.plot(df['timestamp'], df['memory_percent'], label='Memory Usage (%)')

# 标记切换点
for i, row in df.iterrows():
    if not pd.isna(row['state']):
        plt.axvline(row['timestamp'], color='red', linestyle='--', alpha=0.5)
        plt.text(row['timestamp'], row['cpu_usage'] + 5,
                 f"状态:{row['state']}\n原因:{row['reason']}",
                 rotation=90, fontsize=8, color='red', ha='left')

plt.legend()
plt.xlabel('时间')
plt.ylabel('资源占用 (%)')
plt.title('资源使用情况与状态切换')
plt.tight_layout()
plt.show()
