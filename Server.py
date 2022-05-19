from fileinput import filename
import socket, threading
from datetime import datetime
# Setting up the multithreading server
class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.client_socket = clientsocket
        print ("New connection added: ", clientAddress)
    def run(self):
        addr = str(clientAddress[1])
        print ("Connection from : ", addr)

        while True:
            request = self.client_socket.recv(2048).decode()
            print ("from client", request)
            #parsing the request
            headers = request.split('\n')
            fields = headers[0]
            # write http request in a file
            writelog(fields, addr)

            response = handle_request(request)
            self.client_socket.send(response.encode())


# function to write logs and save it in a log file
def writelog(request,address):
    now = datetime.now()
    datestr = now.strftime("%m%d%Y")
    filename = datestr + ".log"
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    logfile = open("logs/"+ filename, "a", encoding="utf-8")
    logfile.write(dt_string + " - " + address + " - " + request + "\n")
    logfile.close()

# function to handle 
def handle_request(request):
    headers = request.split('\n')
    fields = headers[0].split()
    request_type = fields[0]
    filename = fields[1] 
    print('Filename:', filename)
    if request_type =='GET':
        try:
            # convert png file to print out in html file
            if filename =='image.png':
                filename = 'image.html'
            fin = open("files" + filename)
            content = fin.read()
            fin.close()
            response = 'HTTP/1.1 200 OK\n\n' + content 
        except FileNotFoundError:
            response = 'HTTP/1.1 404 Not Found\n\nFile Not Found'
        # except Exception as e:

    else:
        response ='HTTP/1.1 400 Bad Request\n\nRequest Not Supported'
    return response


LOCALHOST = "127.0.0.1"
PORT = 9000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server starts")
print('Listening on port %s... '% PORT)

print("Waiting for client request..")

while True:
    server.listen(1)
    clientConn, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientConn)
    newthread.start()