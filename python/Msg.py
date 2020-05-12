# 心跳包协议
# cmd = 1000, seq = 0
# cmd = 1000, seq = 0

# 注册协议
# cmd = 1001, seq = 0, {"username": "13917043329", "nickname": "balloon", "password": "123"}
# cmd = 1001, seq = 0, {"code": 0, "msg": "ok"}

# 登录协议
# // status: 在线状态 0 离线 1 在线 2 忙碌 3 离开 4 隐身
# // clienttype: 客户端类型, pc = 1, android = 2, ios = 3
# cmd = 1002, seq = 0, {"username": "13917043329", "password": "123", "clienttype": 1, "status": 1}
# cmd = 1002, seq = 0, {"code": 0, "msg": "ok", "userid": 8, "username": "13917043320", "nickname": "zhangyl",
#                       "facetype": 0, "customface": "文件md5", "gender": 0, "birthday": 19891208, "signature": "哈哈，终于成功了",
#                       "address": "上海市东方路3261号", "phonenumber": "021-389456", "mail": "balloonwj@qq.com"}

# 获取用户列表
# cmd = 1003, seq = 0

# 查找用户
# type查找类型 0所有， 1查找用户 2查找群
# cmd = 1004, seq = 0, {"type": 1, "username": "zhangyl"}