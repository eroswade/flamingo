import zlib
import struct
import socket
import select
import protocolstream
import time
import json
def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)

        return instances[cls]
    return _singleton


@singleton
class IUSocket():
    def __init__(self):
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.con.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server = "101.37.25.166"
        self.port = 20000
        self.m_strRecvBuf=b''
        self.m_nHeartbeatSeq = 0
        self.m_Lasttime = time.time()

    def Send(self,str):
        compressed_data = zlib.compress(str)
        originlen = len(str)
        complen = len(compressed_data)

        d = 1
        d = d.to_bytes(1, 'big')
        packed_data = d + originlen.to_bytes(4,'little') + complen.to_bytes(4,'little')

        # \xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xcc
        # \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
        self.m_strSendBuf=packed_data + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + compressed_data
        self._send()

    def Connect(self):
        address = (str(self.server), self.port)
        self.con.connect(address)
        # print('connection ')

    def _send(self):
        self.con.send(self.m_strSendBuf)

    def checkreceived(self):
        read_sockets, write_sockets, error_sockets = select.select([self.con], [], [],1)
        for sock in read_sockets:
            # incoming message from remote server
            if sock == self.con:
                return True
            else:
                return False
        return False

    def Recv(self):
        self.m_strRecvBuf = self.con.recv(10 * 1024)
        if self.m_strRecvBuf:
            originlen = int.from_bytes(self.m_strRecvBuf[1:5], 'little')
            print('origin len %d'%(originlen))
            complen = int.from_bytes(self.m_strRecvBuf[5:9], 'little')
            print('compressed len %d'%(complen))
            print(len(self.m_strRecvBuf[25:]))
            if self.m_strRecvBuf[0] == 1:

                outbuf = zlib.decompress(self.m_strRecvBuf[25:])
                buflen = int.from_bytes(outbuf[0:4], 'big')# == originlen == len(outbuf)
                cmd = int.from_bytes(outbuf[6:10], 'big')
                print('cmd %d' % cmd)
                seg = int.from_bytes(outbuf[10:14], 'big')
                print('seg %d' % seg)

                # print(outbuf)
                # print(int.from_bytes(outbuf[0:4], 'big'))
                # print(int.from_bytes(outbuf[4:8], 'big'))
                # print(int.from_bytes(outbuf[8:12], 'big'))
                # print(int.from_bytes(outbuf[12:16], 'big'))
                self.m_strRecvBuf = outbuf[15:]
            else:
                outbuf = self.m_strRecvBuf[25:]
                self.m_strRecvBuf =  outbuf[15:]
            if len(self.m_strRecvBuf):
                if cmd == 1100:
                    print(json.loads(self.m_strRecvBuf[:-8].decode('unicode-escape')))
                    print('from id %d'%int.from_bytes(self.m_strRecvBuf[-8:-4], 'big'))
                    print('to id %d' % int.from_bytes(self.m_strRecvBuf[-4:], 'big'))
                else:
                    print(json.loads(self.m_strRecvBuf.decode('unicode-escape')))

    def sendheartbeat(self):
        msg_type_beat=1000
        bs = protocolstream.BinaryStreamWriter()
        bs.SendBufConstruct(msg_type_beat, self.m_nHeartbeatSeq, '')
        bs.Flush()
        self.m_nHeartbeatSeq += 1
        self.Send(bs.m_data)

    def RecvThreadProc(self):
        while(1):
            currenttime = time.time()
            nRet = self.checkreceived()
            if(nRet):
                self.m_Lasttime = currenttime
                self.Recv()
            else:
                if currenttime-self.m_Lasttime > 5:
                    self.m_Lasttime = currenttime
                    self.sendheartbeat()
