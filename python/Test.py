import protocolstream
import json
from IUSocket import IUSocket
import threading
import zlib
import time

## 登录测试
msg_type_login=1002
# 构造指令
str = json.dumps({'username':'13575982163','password':'sunshower','clienttype':1,'status':1})
bs = protocolstream.BinaryStreamWriter()
bs.SendBufConstruct(msg_type_login,0,str)
bs.Flush()

# socket
sock = IUSocket()
sock.Connect()
sock.Send(bs.m_data)


threading.Thread(target=sock.RecvThreadProc(), args=())


# msg_type_beat = 1000
# bs = protocolstream.BinaryStreamWriter()
# bs.SendBufConstruct(msg_type_beat, 1, '')
# bs.Flush()
# # b'\x00\x00\x00\x0f\xcc\xcc\x00\x00\x03\xe8\x00\x00\x00\x00\x00'
# sock = IUSocket()
# sock.Send(bs.m_data)

toid = 1249
msgcontext = 'test'
msg = {'msgType':1,'time':time.time(),'clientType':1,'font':['微软雅黑',12,0,0,0,0],'content''':[{'msgText':msgcontext}]}
bs.SendBufConstruct(1100,0,msg)
bs.WriteInt32(toid)
bs.Flush()
sock.Send(bs.m_data)