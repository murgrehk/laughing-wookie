import socket
import _thread
import threading

PRELUDE = "-> "
QUIT_STRING = 'q'


class Client(object):
    def __init__(self,name,host='127.0.0.1',port=5005,buffer_size=1024):
        self.host = host
        self.port = port
        self.name = name
        self.buffer_size = buffer_size
        self.socket = socket.socket()
        self.lock = threading.Lock()
        self.socket.connect((self.host, self.port))
        self.text = ''

    def send_data(self,data):
        self.socket.send(bytes(data, 'UTF-8'))

    def receive_data(self):
        while True:
            try:
                data = self.socket.recv(self.buffer_size).decode('UTF-8')
            except:
                break
            if data:
                self.lock.acquire()
                self.text = data
                self.lock.release()
                return True
        #self.client.close()

    def get_data(self):
        self.lock.acquire()
        ret = self.text
        self.lock.release()
        return ret

    def close_socket(self):
        self.socket.close()

    def run_client(self):
        while True:
            message = input(PRELUDE)
            if not message:
                continue
            if message is not QUIT_STRING:
                self.send_data(message)
                self.receive_data()
                print("Received from server: {}".format(str(self.text)))
                return True
            else:
                self.send_data(message)
                self.receive_data()
                print("Received from server: {}".format(str(self.text)))
                return False

def main():


    client = Client('myname')
    while True:
        if not client.run_client():
            break
    client.close_socket()

if __name__ == '__main__':
    main()

    
