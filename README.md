# 搬瓦工流量监控

这是一个使用 Python 编写的搬瓦工流量监控工具。该工具每 5 分钟请求一次搬瓦工 API，获取多台 VPS 的流量使用情况，并将结果输出到控制台。同时，结果会被存储到本地的 SQLite 数据库中。

## 功能

- 每 5 分钟自动检查搬瓦工流量使用情况
- 支持多台搬瓦工 VPS
- 将数据存储到本地 SQLite 数据库
- 从配置文件中读取 VPS 信息

## 环境要求

- Python 3.6+

## 安装

1. 下载或克隆此项目

2. 在项目根目录下创建一个名为 `conf.ini` 的配置文件，并按照以下格式添加你的搬瓦工 VPS 信息：

   ```
   makefileCopy code
   [machine1]
   veid = 你的veid1
   api_key = 你的api_key1
   
   [machine2]
   veid = 你的veid2
   api_key = 你的api_key2
   
   # ... 添加更多机器信息
   ```

3. 在终端中，导航到项目根目录并运行以下命令以启动监控工具：

   ```
   Copy code
   python bandwagonhost_data_multi.py
   ```

   程序将开始每 5 分钟检查一次搬瓦工流量使用情况，并将结果输出到控制台和本地 SQLite 数据库中。