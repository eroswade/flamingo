from __future__ import print_function

import signal
import pyuv
from time import strftime, gmtime

def getGmt():
    return strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())


def on_read(client, data, error):
    if data is None:
        client.close()
        clients.remove(client)
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

def on_connection(server, error):
    client = pyuv.TCP(server.loop)
    server.accept(client)
    clients.append(client)
    client.start_read(on_read)

def signal_cb(handle, signum):
    [c.close() for c in clients]
    signal_h.close()
    server.close()


print("PyUV version %s" % pyuv.__version__)

loop = pyuv.Loop.default_loop()
clients = []

server = pyuv.TCP(loop)
server.bind(("0.0.0.0", 80))
server.listen(on_connection)

signal_h = pyuv.Signal(loop)
signal_h.start(signal_cb, signal.SIGINT)

loop.run()
print("Stopped!")