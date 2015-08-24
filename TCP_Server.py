import socket
import _thread
import TCP_Client

HOST = ''
PORT = 5005
MAX_CONNECTIONS = 1
QUIT_STRING = TCP_Client.QUIT_STRING

class Server(object):
    def __init__(self,HOST='127.0.0.1',PORT=5005,MAX_CONNECTIONS=2):
        self.HOST = HOST
        self.PORT = PORT
        self.MAX_CONNECTIONS = MAX_CONNECTIONS
        self.text = ''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind(('', self.PORT))
        except socket.error as e:
            print(str(e))
        self.socket.listen(self.MAX_CONNECTIONS)
        self.connections = []

    def threaded_client(self,connection,buffer_size=1024):
        while True:
            try:
                data = connection.recv(buffer_size).decode('UTF-8')
                print('received data')
                print(data)
                data = self.process_data(data)
                print(data)
                print('processed data')
            except:
                print('error receiving data')
                data = ''
            if not data:
                print('no data received')
                break
            for conn,addr in self.connections:
                try:
                    print('sending all')
                    conn.sendall(bytes(data + '\n','UTF-8'))
                    print('sent all')
                except:
                    print('error sending data')
                    #self.connections.remove((conn,addr))
        connection.close()

    def accept_connection(self):
        while True:
            conn, addr = self.socket.accept()
            self.connections.append((conn,addr))
            print("Connection from: {}".format(str(addr)))
            _thread.start_new_thread(self.threaded_client,(conn,))

    def process_data(self,data):
        return data.upper()

    def farewell_message():
        return "Goodbye."

    def handler(client_socket, addr, buffer_size=1024):
        while True:
            data = client_socket.recv(buffer_size).decode('UTF-8')
            if data is not QUIT_STRING:
                print('received: {}'.format(data))
                if not data:
                    break
                data = process_data(data)
                client_socket.send(bytes(data, 'UTF-8'))
                # print('sent: {}'.format(repr(data)))
            else:
                print('{} is quitting'.format(str(addr)))
                client_socket.send(bytes(farewell_message(), 'UTF-8'))
                break
        client_socket.close()

# def run_server(connection, buffer_size=1024):
#     data = connection.recv(buffer_size).decode('UTF-8')
#     if not data:
#         return False
#     print("from connected user: {}".format(str(data)))
#     data = process_data(data)
#     print("sending: {}".format(str(data)))
#     connection.send(bytes(data,'UTF-8'))
#     return True

def main():
    server = Server()
    
    while True:
        server.accept_connection()
    #     if not run_server(client_socket,1024):
    #         break
    # client_socket.close()

if __name__ == '__main__':
    main()
