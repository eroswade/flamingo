# 使用说明

## 依赖
1. redis
2. qq第5代. web插件. (接收消息)
3. 酷Q + 插件(发送消息)(可选,如果不需要发消息,就用不到)
4. python 依赖:
    1. apsw
    2. redis
    3. pyuv

## 安装说明:
1. redis下载 
https://github.com/microsoftarchive/redis/releases
2. python 
    1. apsw
        https://rogerbinns.github.io/apsw/download.html
        如果安装在默认python下,但运行不是默认PYTHON, 把它从目录里拷出来就好了
    2. redis
        pip install redis
    3. pyuv 
        pip install pyuv

## 配置
1. 启动redis
redis-server.exe redis.windows.conf
2. 启动服务器
activate webspider & python Main.py
3. 启动 QQ
4. 启动酷Q(可选,如果不需要发消息,就用不到)