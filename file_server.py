import socket
import threading
import os

host = '127.0.0.1'
port = 5002

def setup(host='127.0.0.1',port=5002):
    host = host
    port = port

def retrieve_file(name, socket, buffer_size=1024):
    file_name = socket.recv(buffer_size).decode('UTF-8')
    if os.path.isfile(file_name):
        socket.send(bytes(str(os.path.getsize(file_name)), 'UTF-8'))
        response = socket.recv(buffer_size).decode('UTF-8')
        if response.startswith('Y'):
            with open(file_name, 'rb') as f:
                bytes_to_send = f.read(buffer_size).decode('UTF-8')
                socket.send(bytes(bytes_to_send, 'UTF-8'))
    else:
        socket.send(bytes("-1", 'UTF-8'))
    socket.close()

def run_server(socket):
    c, addr = socket.accept()
    print("Client connected from IP: {}".format(str(addr)))
    t = threading.Thread(target=retrieve_file, args=("retrieve_file", c))
    t.start()

def main():
    setup()

    s = socket.socket()
    s.bind(('',port))

    s.listen(5)
    print("File server started.....")

    while True:
            run_server(s)
    s.close()

if __name__ == '__main__':
    main()
