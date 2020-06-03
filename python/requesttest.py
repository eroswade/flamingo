import requests

sess = requests.Session()


url = 'http://127.0.0.1/test.html'
# 'Event=NormalIM&Sender=18467184&SenderName=Eros.Wade&SendTime=1591154210&Message=中文测试&RobotQQ=2130271802'
f = {
        "Event": 'NormalIM',
        "Sender": '18467184',
        "SenderName": 'Eros.Wade',
        'SendTime':'1591154210',
        'Message':'中文测试',
        'RobotQQ':'2130271802'
    }
f = {
        "Event": 'ClusterIM',
'GroupId': '923883633',
'GroupName': '韵达暴风后的祈祷',
        "Sender": '18467184',
        "SenderName": 'Eros.Wade',
        'SendTime':'1591154210',
        'Message':'好的谢谢',
        'RobotQQ':'2130271802'
    }
result = sess.get(url, data = f)
print(result)