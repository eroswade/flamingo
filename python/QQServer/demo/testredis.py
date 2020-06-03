import redis

rs = redis.Redis(host = '127.0.0.1',port=6379,db=0)
requestmsg = {'User':'eros',}
if requestmsg.__contains__('User'):
    if rs.exists(requestmsg['User']):
        rs.get(requestmsg['User'])
    else:
        rs.sadd(requestmsg['User'], 0, 0)