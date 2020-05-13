import protocolstream
import json

## 构造指令
str = json.dumps({'username':'17357942163','password':'sunshower','clienttype':1,'status':1})
bs = protocolstream.BinaryStreamWriter()
bs.SendBufConstruct(1002,0,str)

bs.Flush()
print(bs.m_data)

## 发送数据
from IUSocket import IUSocket

sock = IUSocket()
sock.Connect()
sock.Send(bs.m_data)
