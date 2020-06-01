import socket
import json
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #声明socket类型，同时生成链接对象
client.connect(('127.0.0.1',20005)) #建立一个链接，连接到本地的6969端口


req_message = {'qqid': 18467184, 'message': '中文测试'}
sendstr = json.dumps(req_message)
client.send(sendstr.encode('utf-8'))  #发送一条信息 python3 只接收btye流
data = client.recv(1024) #接收一个信息，并指定接收的大小 为1024字节
print('recv:',data.decode('utf-8')) #输出我接收的信息
client.close()