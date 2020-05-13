import zlib
import struct
import socket

class IUSocket():
    def __init__(self):
        self.con = socket.socket()
        self.server = '101.37.25.166'
        self.port = 20000
    def Send(self,str):
        compressed_data = zlib.compress(str)
        originlen = len(str)
        complen = len(compressed_data)

        d = 1
        d = d.to_bytes(1, 'big')
        values = (d,originlen,complen)
        s = struct.Struct('cII') #  I4: unsigned int s: char* f:float p:char* c: char i: int
        packed_data = s.pack(*values)
        # unpacked_data = s.unpack(packed_data)

        # \x01\x00\x00\x00a\x00\x00\x00[\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00x\x9cc``Hd\x00\x02\xe6W 2\xa8Z\xa9\xb48\xb5(/17U\xc9JA\xc9\xd0\xdc\xd8\xd4\xdc\xd2\xc4\xc8\xd0\xccXIGA\xa9 \xb1\xb8\xb8<\xbf(\x05$U\\\x9aW\x9c\x91_\x9eZ\x04\x92H\xce\xc9L\xcd+)\xa9,\x00\xe92\x04\n\x14\x97$\x96\x94\x16\x838\xb5\x00\x93~\x1a\xc5
        d = 0
        self.m_strSendBuf=packed_data + d.to_bytes(16,'big') + compressed_data

        self._send()

    def Connect(self):
        self.con.connect((self.server,self.port))

    def _send(self):
        self.con.send(self.m_strSendBuf)
        data = self.con.recv(1024)
        print('recv:', data.decode())