from threading import Thread

import apsw
import multiprocessing


class SingleThreadOnly(object):
    def __init__(self, db):
        self.db = apsw.Connection(db)
        self.cursor = self.db.cursor()

    def execute(self, req, arg=None):
        self.cursor.execute(req, arg or tuple())

    def select(self, req, arg=None):
        self.execute(req, arg)
        for raw in self.cursor:
            yield raw

    def close(self):
        self.db.close()


class MultiThreadOK(Thread):
    def __init__(self, dbname):
        super(MultiThreadOK, self).__init__()
        self.dbname = dbname
        self.reqs = multiprocessing.Queue()
        self.start()

    def run(self):
        db = apsw.Connection(self.dbname)
        cursor = db.cursor()
        print('start run')
        while True:
            req, arg, res = self.reqs.get()
            if req == '--close--': break
            cursor.execute(req, arg)
            if res:
                for rec in cursor:
                    res.put(rec)
                res.put('--no more--')
        print('close db')
        db.close()

    def execute(self, req, arg=None, res=None):
        print('execute')
        self.reqs.put((req, arg or tuple(), res))

    def select(self, req, arg=None):
        manager = multiprocessing.Manager()
        queue = manager.Queue()
        self.execute(req, arg, queue)
        while True:
            rec = queue.get()
            if rec == '--no more--': break
            yield rec

    def close(self):
        self.execute('--close--')
        print('close')


if __name__ == '__main__':

    db = 'msg.db'
    multithread = True

    if multithread:
        sql = MultiThreadOK(db)
    else:
        sql = SingleThreadOnly(db)

    sql.execute('CREATE TABLE "MSG" ("id"INTEGER PRIMARY KEY AUTOINCREMENT,	"type"	INTEGER,	"sender"	INTEGER,	"sendername"	TEXT,	"groupid"	INTEGER,	"groupname"	TEXT,	"sendtime"	INTEGER,	"message"	TEXT);')
    sql.execute('INSERT INTO "main"."MSG"("type","sender","sendername","groupid","groupname","sendtime","message") VALUES (1,1234,"test",12341324,"asdkdsf",123412134,"asdfkasdfk");')
    # sql.execute("insert into people values(?,?)", ('TORVALDS', 'Linus'))
    # for f, n in sql.select("select first, name from people"):
    #     print(f, n)
    sql.close()