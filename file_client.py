import socket

host = '127.0.0.1'
port = 5000
prelude = "-> "
quit_string = 'q'

def setup(host='127.0.0.1',port=5000):
    host = host
    port = port

def main():
	s = socket.socket()
	s.connect((host,port))

	file_name = input("File name? {}".format(prelude))
	if file_name is not quit_string:
		s.send(bytes(file_name, 'UTF-8'))
		data = s.recv(1024).decode('UTF-8')
		if not data.startswith('-1'):
			file_size = float(data)
			message = input("The file size is {} bytes. Download? (Y/N) {}".format(str(file_size), prelude))

			if message.upper().startswith('Y'):
				s.send(bytes(message, 'UTF-8'))
				f = open('new_{}'.format(file_name), 'wb')
				data = s.recv(1024).decode('UTF-8')
				total_data_received = len(data)
				f.write(bytes(data, 'UTF-8'))
				while total_data_received < file_size:
					data = s.recv(1024).decode('UTF-8')
					total_data_received += len(data)
					f.write(bytes(data, 'UTF-8'))
					print("{0:.2f}%% done".format((100.0*total_data_received/file_size)))
				print("Download complete!")
		else:
			print("File does not exist.")
	s.close()

if __name__ == '__main__':
	main()