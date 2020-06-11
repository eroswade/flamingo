import socket
import json
import urllib.parse


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #声明socket类型，同时生成链接对象
client.connect(('127.0.0.1',20005)) #建立一个链接，连接到本地的6969端口
req_message = {'qqid': 18467184, 'message': '中文测试'}
req_message = {'groupid':27361142, 'message': 'test'}
sendstr = json.dumps(req_message)
client.send(sendstr.encode('utf-8'))  #发送一条信息 python3 只接收btye流
data = client.recv(20000) #接收一个信息，并指定接收的大小 为1024字节 如果没接收完. WHILE循环继续接收.
print(data)

# client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #声明socket类型，同时生成链接对象
# client.connect(('127.0.0.1',20006)) #建立一个链接，连接到本地的6969端口
# req_message = {
#     'User': 'eros', # 注意,这个ID必须有. 用来区分哪个ID进来查询.
#     'SQLidfrom': 0,# 这个参数如果没有, 会找最新的数据
#     'SQLgroupid':12341324, # 分群号查询
#     'SQLsender':1234,# 分QQ号查询
#     'SQLsendername':'test', # 分QQ昵称查询
#     'SQLgroupname':'asdkdsf',# 分群名查询
#     'SQLsendtime': 123145 } # 时间大于一个时间戳
# # 'SQLidfrom': 0,
# # 'SQLgroupid':12341324,
# # 'SQLsender':1234,
# # 'SQLsendername':'test',
# # 'SQLgroupname':'asdkdsf',
# # 'SQLsendtime': 123145 # 时间大于一个时间戳
# sendstr = json.dumps(req_message)
# client.send(sendstr.encode('utf-8'))  #发送一条信息 python3 只接收btye流
# data = client.recv(20000) #接收一个信息，并指定接收的大小 为1024字节 如果没接收完. WHILE循环继续接收.
# jsdata = json.loads((data.decode()))
# print(jsdata['row'])
# if jsdata['row']>0:
#     print(jsdata['list'][0])
# client.close()