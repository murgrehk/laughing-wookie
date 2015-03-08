import socket
import TCP_Client
import signal

host = ''
port = 0
buffer_size = 1024
prelude = "-> "
quit_string = "QUIT"

class AlarmException(Exception):
	pass

def alarmHandler(signum, frame):
	raise AlarmException

def nonBlockingRawInput(prompt='', timeout=5):
	signal.signal(signal.SIGALRM, alarmHandler)
	signal.alarm(timeout)
	try:
		data = input(prompt)
		signal.alarm(0)
		return data
	except AlarmException:
		print()
	signal.signal(signal.SIGALRM, signal.SIG_IGN)
	return ''

def main():

	host, port = TCP_Client.setup(host='127.0.0.1', port=5001)
	print(host, port)

	client_socket = socket.socket()
	client_socket.connect((host,port))
	

	username = input("Name {}".format(prelude))
	#username = ''.join(("NAME::",username.upper()))
	username = 'NAME::{}'.format(username.upper())
	client_socket.send(bytes(username, 'UTF-8'))
	username_response = client_socket.recv(buffer_size).decode('UTF-8')
	#prelude = ' '.join((username_response, prelude))
	prelude = '{} {}'.format(username_response, prelude)
	print("username response: {}".format(username_response))
	client_socket.setblocking(0)

	while True:
		try:
			incoming_data = client_socket.recv(buffer_size).decode('UTF-8')
			print("Incoming data {}".format(incoming_data))

		except socket.error:
			pass
		try:
			data = nonBlockingRawInput(prelude,1)
			if not data:
				continue
			if data.upper() == quit_string.upper():
				break
			else:
				#data = ''.join((prelude,data))
				data = '{}{}'.format(prelude,data)
				client_socket.send(bytes(data, 'UTF-8'))
				# data = client_socket.recv(buffer_size).decode('UTF-8')
				# if not data:
				# 	break
				# else:
				# 	print(data)
		except socket.error:
			pass
	client_socket.close()

if __name__ == '__main__':
	main()