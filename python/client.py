import pyuv

def on_close(tcp):
    print ("closed")

def on_read(tcp, data,error):
    print ("read")
    if data is None:
        tcp.close(on_close)
    else:
        print(data)

def on_write(tcp, status):
    print ("written")
    tcp.start_read(on_read)

def on_connection(tcp, status):
    print ("connected")
    req_message = b"GET / HTTP/1.0\r\n\r\n"
    tcp.write(req_message, on_write)

def main():
    server_addr = ("127.0.0.1", 1234)
    loop = pyuv.Loop.default_loop()
    tcp = pyuv.TCP(loop)

    tcp.connect(server_addr, on_connection)
    print("main")
    loop.run()

if __name__ == "__main__":
    main()