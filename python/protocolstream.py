import socket
import struct

# b1 = chr((n & 0xff000000) >> 24)
# b2 = chr((n & 0xff0000) >> 16)
# b3 = chr((n & 0xff00) >> 8)
# b4 = chr(n & 0xff)
# s = b1 + b2 + b3 + b4

class BinaryStreamWriter():
    def __init__(self):
        self.m_data = b''
        self.cur = 0
    def WriteInt32(self,i):
        i2 = 999999999
        i2 = socket.htonl(i)
        s = struct.pack('>I', i2)
        self.m_data = self.m_data + s

    def SendBufConstruct(self,cmd,seg,msg):
        self.WriteInt32(cmd)
        self.WriteInt32(seg)
        self.WriteCString(msg)

    def WriteCString(self,str):
        length = self.write7BitEncoded(len(str))
        self.m_data = self.m_data + length
        self.m_data = self.m_data + str.encode('utf-8')

    def write7BitEncoded(self,str):
        return str

    def read7BitEncoded(self,buf):
        value = buf
        return value

    def ReadInt32(self):
        d = self.m_data[self.cur:self.cur + 4]
        s = struct.unpack('>I', d)
        code = socket.ntohl(s[0])
        self.cur = self.cur + 4
        return code

    def ReadLengthWithoutOffset(self):
        buf = self.m_data[self.cur:self.cur+4]
        retlen = self.read7BitEncoded(buf)
        return retlen

    def ReadString(self):
        length = self.ReadLengthWithoutOffset()

        str = self.m_data[self.cur : self.cur+length]

        self.cur = self.cur + length

        return str

