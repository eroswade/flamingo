from __future__ import print_function

import signal
import pyuv
from time import strftime, gmtime
from threading import Thread

def getGmt():
    return strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())

class Server():
    def __init__(self):
        self.clients=[]
    def on_read(self,client, data, error):
        if data is None:
            client.close()
            self.clients.remove(client)
            print('remove one client')
            return
        print(data)

        ## origin demo: echo server
        # client.write(data)

        ## new demo
        # HTTP response
        # 怎么制造HTTP协议回应: https://www.cnblogs.com/an-wen/p/11180076.html
        respone = 'HTTP/1.1 200 OK\r\n Date:'
        dt = getGmt()
        respone = respone + dt + '\r\n'
        Conttent = 'asdfasdf'
        respone = respone + 'Content-Length:' + str(len(Conttent)) + '\r\n' + 'Content-Type: text/html \r\n\r\n'
        respone = respone + Conttent

        client.write(respone.encode())

    def on_connection(self,server, error):
        client = pyuv.TCP(server.loop)
        server.accept(client)
        self.clients.append(client)
        client.start_read(self.on_read)

    def signal_cb(self,handle, signum):
        [c.close() for c in self.clients]
        self.signal_h.close()
        self.server.close()

    def runhttp(self):# test by requesttest
        print("PyUV version %s" % pyuv.__version__)

        self.loop = pyuv.Loop.default_loop()

        self.server = pyuv.TCP(self.loop)
        self.server.bind(("0.0.0.0", 80))
        self.server.listen(self.on_connection)

        self.signal_h = pyuv.Signal(self.loop)
        self.signal_h.start(self.signal_cb, signal.SIGINT)

        self.loop.run()

serv = Server()
th = Thread(target=serv.runfunction())
print("Stopped!")