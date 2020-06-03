

import urllib.parse
str = 'Event=NormalIM&Sender=18467184&SenderName=Eros.Wade&SendTime=1591154210&Message=中文测试&RobotQQ=2130271802'

if str.startswith('Event'):
    parms = urllib.parse.parse_qsl(str)
    print(parms['Event'])

