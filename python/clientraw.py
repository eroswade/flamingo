import socket
import json
import urllib.parse
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #声明socket类型，同时生成链接对象
client.connect(('127.0.0.1',20006)) #建立一个链接，连接到本地的6969端口


# req_message = {'qqid': 18467184, 'message': '中文测试'}
req_message = {'groupid': 27361142, 'message': '中文测试'}
sendstr = json.dumps(req_message)
client.send(sendstr.encode('utf-8'))  #发送一条信息 python3 只接收btye流
data = client.recv(20000) #接收一个信息，并指定接收的大小 为1024字节
jsdata = json.loads((data.decode()))
print(jsdata['row'])
print(jsdata['list'][0])
client.close()