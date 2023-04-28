import requests
import json
import time
import sqlite3
import configparser
from datetime import datetime

# 读取配置文件
config = configparser.ConfigParser()
config.read("conf.ini")

# 从配置文件中获取多台搬瓦工机器的 API 信息
machines = [
    {
        "veid": config.get(machine, "veid"),
        "api_key": config.get(machine, "api_key")
    }
    for machine in config.sections()
]

# 创建数据库连接
conn = sqlite3.connect("bwg.db")
cursor = conn.cursor()

# 创建数据表
cursor.execute("""
CREATE TABLE IF NOT EXISTS bwg (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    veid INTEGER,
    plan_monthly_data REAL,
    data_counter REAL,
    hostname TEXT,
    data_next_reset TEXT,
    timestamp TEXT
)
""")
conn.commit()

def get_bandwagonhost_data(veid, api_key):
    url = f"https://api.64clouds.com/v1/getLiveServiceInfo?veid={veid}&api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)

        # 获取所需信息
        plan_monthly_data = data['plan_monthly_data'] / (1024 ** 2)  # 转换为 MB
        data_counter = data['data_counter'] / (1024 ** 2)  # 转换为 MB
        hostname = data['hostname']
        data_next_reset = data['data_next_reset']

        # 将流量重置日期转换为 "2022-01-01" 格式
        data_next_reset_formatted = datetime.fromtimestamp(data_next_reset).strftime('%Y-%m-%d')

        # 打印日志
        print(f"主机名: {hostname}")
        print(f"每月总流量: {plan_monthly_data:.2f} MB")
        print(f"当月使用流量: {data_counter:.2f} MB")
        print(f"流量重置日期: {data_next_reset_formatted}")
        print("\n")

        # 保存到数据库
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
        INSERT INTO bwg (veid, plan_monthly_data, data_counter, hostname, data_next_reset, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (veid, plan_monthly_data, data_counter, hostname, data_next_reset_formatted, timestamp))
        conn.commit()
    else:
        print("请求失败，请检查 veid 和 api_key 是否正确。")

while True:
    for machine in machines:
        get_bandwagonhost_data(machine['veid'], machine['api_key'])
    time.sleep(300)  # 每 5 分钟请求一次

# 关闭数据库连接
cursor.close()
conn.close()
