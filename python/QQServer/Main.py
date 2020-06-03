from __future__ import print_function

import signal
import pyuv
from time import strftime, gmtime
from threading import Thread
import SQLMulti
import urllib.parse

def getGmt():
    return strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())

class HttpServer():
    def __init__(self):
        self.clients=[]
        self.sql = SQLMulti.MultiThreadOK('test.db')
    def on_read(self,client, data, error):
        if data is None:
            client.close()
            self.clients.remove(client)
            print('remove one client')
            return
        print('message coming')
        strin = urllib.parse.unquote(data.decode())
        if strin.startswith('Event'):
            parms = urllib.parse.parse_qsl(strin)
            print(parms)

        ## origin demo: echo server
        # client.write(data)

        ## new demo
        # HTTP response
        # 怎么制造HTTP协议回应: https://www.cnblogs.com/an-wen/p/11180076.html
        respone = 'HTTP/1.1 200 OK\r\n Date:'
        dt = getGmt()
        respone = respone + dt + '\r\n'
        Conttent = ''
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
        self.sql.close()

    def runhttp(self):# test by requesttest
        print("PyUV version %s" % pyuv.__version__)

        self.loop = pyuv.Loop.default_loop()

        self.server = pyuv.TCP(self.loop)
        self.server.bind(("0.0.0.0", 80))
        self.server.listen(self.on_connection)

        self.signal_h = pyuv.Signal(self.loop)
        self.signal_h.start(self.signal_cb, signal.SIGINT)

        self.loop.run()


class Server():
    def __init__(self):
        self.clients=[]
        self.sql = SQLMulti.MultiThreadOK('test.db')
    def on_read(self,client, data, error):
        if data is None:
            client.close()
            self.clients.remove(client)
            print('remove one client')
            return
        print(data)

        ## origin demo: echo server
        client.write(data)

    def on_connection(self,server, error):
        client = pyuv.TCP(server.loop)
        server.accept(client)
        self.clients.append(client)
        client.start_read(self.on_read)

    def signal_cb(self,handle, signum):
        [c.close() for c in self.clients]
        self.signal_h.close()
        self.server.close()
        self.sql.close()

    def runserver(self):# test by requesttest
        print("PyUV version %s" % pyuv.__version__)

        self.loop = pyuv.Loop.default_loop()

        self.server = pyuv.TCP(self.loop)
        self.server.bind(("0.0.0.0", 20005))
        self.server.listen(self.on_connection)

        self.signal_h = pyuv.Signal(self.loop)
        self.signal_h.start(self.signal_cb, signal.SIGINT)

        self.loop.run()

threads = []


httpserv = HttpServer()
th = Thread(target=httpserv.runhttp,args=[])


serv = Server()
th2 = Thread(target=serv.runserver)

th.start()
th2.start()
threads.append(th)
threads.append(th2)


# input("Press Enter to continue...")
# serv.signal_cb()
# httpserv.signal_cb()
for t in threads:
    t.join()
print("Stopped!")