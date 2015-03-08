import socket
import TCP_Server
import _thread

host = ''
port = 0
max_connections = 5

clients = []

def process_data(data):
	print(data)
	return data

def handler(client_socket, client_addr, buffer_size=1024):
	print("New connection from: {}".format(str(client_addr)))
	clients.append(client_socket)
	while True:
		data = client_socket.recv(buffer_size).decode('UTF-8')
		if not data:
			break
		elif data.startswith("NAME::"): # someone just connected
			message = data.split("NAME::",1)[1] # get the user's name
			client_socket.send(bytes(message, 'UTF-8'))
			message = "{} has joined the chat.".format(message)
			for client in clients:
				client.send(bytes(message, 'UTF-8'))
		else: # this is a normal chat message
			if data.strip():
				data = process_data(data)
				data = data.split("->")[1]
				data = data.strip()
				#message = "You sent me: {}".format(data)
				#message = "You sent me: {}".format(data.split("->")[1].strip())
				#client_socket.send(bytes(message, 'UTF-8'))
				if data:
					for client in clients:
						client.send(bytes(data, 'UTF-8'))
	client_socket.close()

def main():
	host, port = TCP_Server.setup(host='127.0.0.1', port=5001)
	print(host, port)

	server_socket = socket.socket()
	server_socket.bind((host,port))

	server_socket.listen(max_connections)

	TCP_Server.process_data = process_data

	while True:
		client_socket, addr = server_socket.accept()
		_thread.start_new_thread(handler, (client_socket, addr))
	c.close()


if __name__ == '__main__':
	main()