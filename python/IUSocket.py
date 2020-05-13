import zlib
import struct
import socket

class IUSocket():
    def __init__(self):
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "101.37.25.166"
        self.port = 20000
    def Send(self,str):
        compressed_data = zlib.compress(str)
        originlen = len(str)
        complen = len(compressed_data)

        d = 1
        d = d.to_bytes(1, 'big')
        packed_data = d + originlen.to_bytes(4,'little') + complen.to_bytes(4,'little')
        # unpacked_data = s.unpack(packed_data)

        # b"\x01a\x00\x00\x00^\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00x\x9cc``H<s\x86\x81\x81\xf9\x15\x03\x10\x04U+\x95\x16\xa7\x16\xe5%\xe6\xa6*Y)(\x19\x1a\x9b\x9a\x9bZZ\x18\x19\x9a\x19+\xe9((\x15$\x16\x17\x97\xe7\x17\xa5\x80\xa4\x8aK\xf3\x8a3\xf2\xcbS\x8b@\x12\xc99\x99\xa9y%%\x95\x05 ]\x86@\x81\xe2\x92\xc4\x92\xd2b\x10\xa7\x16\x00'k\x1c_"
        self.m_strSendBuf=packed_data + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + compressed_data
        # print(zlib.decompress(compressed_data))
        self._send()

    def Connect(self):
        address = (str(self.server), self.port)
        self.con.connect(address)
        # print('connection ')

    def _send(self):
        ret = self.con.sendall(self.m_strSendBuf)
        data = self.con.recv(1024)

        print('received: ')
        print(data)

        # data = self.con.recv(1024)
        # print('recv:', data.decode())