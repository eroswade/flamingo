import protocolstream
import json
from IUSocket import IUSocket

# ## 登录测试
# msg_type_login=1002
# # 构造指令
# str = json.dumps({'username':'17357942163','password':'sunshower','clienttype':1,'status':1})
# bs = protocolstream.BinaryStreamWriter()
# bs.SendBufConstruct(msg_type_login,0,str)
# bs.Flush()
#
# # socket
# sock = IUSocket()
# sock.Connect()
# sock.Send(bs.m_data)

## 心跳测试
msg_type_beat=1000
# 构造指令
bs = protocolstream.BinaryStreamWriter()
bs.SendBufConstruct(msg_type_beat,0,'')
bs.Flush()

# socket
sock = IUSocket()
sock.Connect()
sock.Send(bs.m_data)
