import socket
import numpy as np
from tensorflow import keras

HOST = '127.0.0.1'
PORT = 5736
THRESHOLD = 80

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()
client_socket, addr = server_socket.accept()
print('Connected by ', addr)

X_1 = np.zeros(6)

autoencoder = keras.models.load_model('autoencoder_model')
timestep = 1
prev_data = {
        1 : np.zeros([1,4]),
        2 : np.zeros([1,4]),
        3 : np.zeros([1,4]),
        4 : np.zeros([1,4]),
        5 : np.zeros([1,4]),
        6 : np.zeros([1,4]),
        7 : np.zeros([1,4]),
        8 : np.zeros([1,4])
    }

while True:
    data = client_socket.recv(569)

    print('.', end=' ')
    timestep += 1

    if not data:
        break

    try:
        data = list(map(float, data.decode().split(', ')[:-1]))
    except:
        continue

    data = {i+1:np.expand_dims(data[6*i+2:6*(i+1)], axis=0) for i in range(8)}

    new_data = {k:data[k]-prev_data[k] for k in data}

    prev_data = data

    prds = {i+1:autoencoder.predict(new_data[i+1],verbose=0) for i in range(8)}

    errors = {i+1:np.mean(np.power(new_data[i+1]-prds[i+1], 2), axis=1) for i in range(8)}

    for i in range(8):
        if errors[i+1] > THRESHOLD:
            print()
            print(f"[Time:{timestep}] Suspicious Signal on Channel[{i+1}] (Autoencoder Error : {errors[i+1]})")

client_socket.close()
server_socket.close()