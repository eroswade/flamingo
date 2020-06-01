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
tr = threading.Thread(target=sock.RecvThreadProc, args=())
tr.start()


toid = 268435654
msgcontext = 'test'
msg = {'msgType':1,'time':time.time(),'clientType':1,'font':['微软雅黑',12,0,0,0,0],'content''':[{'msgText':msgcontext}]}
bs.clear()
bs.SendBufConstruct(1100,0,json.dumps(msg))
bs.WriteInt32(toid)
bs.Flush()
sock.Send(bs.m_data)

