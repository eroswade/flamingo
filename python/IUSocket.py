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
        values = (1,originlen,complen)
        s = struct.Struct('cI4I4') #  I4: unsigned int s: char* f:float p:char* c: char i: int
        packed_data = s.pack(*values)
        unpacked_data = s.unpack(packed_data)

        self.m_strSendBuf=packed_data + compressed_data

        self._send()

    def Connect(self,ip,port):
        self.con.connect(ip,port)
        print(self.con.recv(1024))

    def _send(self):
        self.con.send(self.m_strSendBuf)
        data = self.con.recv(1024)
        print('recv:', data.decode())