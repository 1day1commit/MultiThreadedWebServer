import socket

SERVER = "127.0.0.1"
PORT = 9000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
req = input("input HTTP request: \n")
client.sendall(req.encode())

while True:
  in_data =  client.recv(1024)
  print("From Server :" ,in_data.decode())
  out_data = input()
  client.sendall(bytes(out_data,'UTF-8'))
  # client can end the program
  if out_data == 'bye':
    break
client.close()