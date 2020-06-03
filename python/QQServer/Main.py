from __future__ import print_function

import signal
import pyuv
from time import strftime, gmtime
from threading import Thread
import SQLMulti
import urllib.parse
import json
import redis

def getGmt():
    return strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())

class HttpServer():
    def __init__(self):
        self.clients=[]
        self.sql = SQLMulti.MultiThreadOK('msg.db')
    def on_read(self,client, data, error):
        if data is None:
            client.close()
            self.clients.remove(client)
            return
        strin = urllib.parse.unquote(data.decode())
        if strin.startswith('Event'):
            parms = urllib.parse.parse_qsl(strin)
            strin = {ip[0]: ip[1] for ip in parms}
            if strin['Event'] != 'Get':
                if strin['Event'] == 'ClusterIM':
                    sqlstring = 'INSERT INTO "main"."MSG"("type","sender","sendername","groupid","groupname","sendtime","message") VALUES (1,%s,\"%s\",%s,\"%s\",%s,\"%s\");'%(
                        strin['Sender'],strin['SenderName'],strin['GroupId'],strin['GroupName'],strin['SendTime'],strin['Message'])
                elif strin['Event'] == 'NormalIM':
                    sqlstring = 'INSERT INTO "main"."MSG"("type","sender","sendername","groupid","groupname","sendtime","message") VALUES (2,%s,\"%s\",NULL,NULL,%s,\"%s\");'%(
                        strin['Sender'], strin['SenderName'],  strin['SendTime'],strin['Message'])
                self.sql.execute(sqlstring)

        # 群消息:
        # {'Event': 'ClusterIM', 'GroupId': '923883633', 'GroupName': '韵达暴风后的祈祷',
        # 'Sender': '2696687334', 'SenderName': '觉觉', 'SendTime': '1591162531',
        # 'Message': '4305931900659 == == 派件网点在哪里客户想要自取了', 'RobotQQ': '2130271802'}
        # 私聊消息：
        # {'Event': 'NormalIM', 'Sender': '18467184', 'SenderName': 'Eros.Wade',
        # 'SendTime': '1591162451', 'Message': 'asdf', 'RobotQQ': '2130271802'}

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
        self.sql = SQLMulti.SingleThreadOnly('msg.db')
        self.rs = redis.Redis(host = '127.0.0.1',port=6379,db=0)
    def on_read(self,client, data, error):
        if data is None:
            client.close()
            self.clients.remove(client)
            print('remove one client')
            return

        requestmsg = json.loads(data)
        curid = 0
        wherestr = ''
        if requestmsg.__contains__('User'):
            # self.rs.delete('ushash')
            if requestmsg.__contains__('SQLidfrom'):
                curid = int(requestmsg['SQLidfrom'])
                self.rs.hset(requestmsg['User'],'id',curid)
            else:
                if self.rs.exists(requestmsg['User']):
                    curid = int(self.rs.hget(requestmsg['User'],'id'))
                else:
                    self.rs.hset(requestmsg['User'],'id',0)
                    curid = 0
            if requestmsg.__contains__('SQLgroupid'):
                wherestr = wherestr + ' AND groupid=%s '%(requestmsg['SQLgroupid'])
            if requestmsg.__contains__('SQLgroupname'):
                wherestr = wherestr + ' AND groupname="%s" '%(requestmsg['SQLgroupname'])
            if requestmsg.__contains__('SQLsender'):
                wherestr = wherestr + ' AND sender=%s ' % (requestmsg['SQLsender'])
            if requestmsg.__contains__('SQLsendername'):
                wherestr = wherestr + ' AND sendername="%s" ' % (requestmsg['SQLsendername'])
            if requestmsg.__contains__('SQLsendtime'):
                wherestr = wherestr + ' AND sendtime>%s ' % (requestmsg['SQLsendtime'])

        sqlresult = self.sql.select("select * from MSG where id>%d"%(int(curid)) + wherestr)
        jsonlist = []
        rowcount = 0
        mxid = curid
        for id, type, sender,sendername,groupid,groupname,sendtime,message in sqlresult:
            # print(id, type, groupid,groupname,sender,sendername,sendtime,message)
            dic = {'id':id,'type':type,'groupid':groupid,'groupname':groupname,'sender':sender,'sendername':sendername,'sendtime':sendtime,'message':message}
            jsonlist.append(dic)
            rowcount += 1
            if id > mxid:
                mxid = id

        if requestmsg.__contains__('User'):
            self.rs.hset(requestmsg['User'], 'id', mxid)

        outdic = {'row':rowcount,'list':jsonlist}

        # origin demo: echo server
        client.write(json.dumps(outdic).encode())

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
        self.server.bind(("0.0.0.0", 20006))
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