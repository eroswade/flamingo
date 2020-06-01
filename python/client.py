import pyuv
import json

def on_close(tcp):
    print ("closed")

def on_read(tcp, data,error):
    print ("read")
    if data is None:

        tcp.close(on_close)
    else:
        print(data.decode('utf-8'))

def on_write(tcp, status):
    print ("written")
    tcp.start_read(on_read)

def on_connection(tcp, status):
    print ("connected")
    req_message = {'groupid':27361142,'message':'asdflkasdf'}
    sendstr = json.dumps(req_message)
    tcp.write(bytes(sendstr,encoding='utf8'), on_write)

def main():
    server_addr = ("127.0.0.1", 20005)
    loop = pyuv.Loop.default_loop()
    tcp = pyuv.TCP(loop)

    tcp.connect(server_addr, on_connection)
    print("main")
    loop.run()

if __name__ == "__main__":
    main()