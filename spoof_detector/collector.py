import socket
import re
import sys
import os

HOST = '127.0.0.1'
PORT = 5736

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()
client_socket, addr = server_socket.accept()
print('Connected by ', addr)

f = open(os.path.join('data', sys.argv[1]), "w")

i = 1
while True:
    data = client_socket.recv(800)

    if not data:
        break

    line = data.decode()
    line = re.sub(r'[^\x00-\x7F]', '', line)
    print('H',line, 'F')

    i += 1

    if i <= 8:
        continue
    f.write(line)

f.close()
client_socket.close()
server_socket.close()