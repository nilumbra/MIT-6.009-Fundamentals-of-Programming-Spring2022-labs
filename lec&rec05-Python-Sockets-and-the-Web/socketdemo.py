import socket

HOSTNAME = ''
PORT = 6009

# create a socket, bind it to the port given above, and start listening for
# connections
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.bind((HOSTNAME, PORT))
my_socket.listen()

#wait for someone to connect
print('waiting for connection')
connected_socket, addr = my_socket.accept()
print('received connection from', addr)

# send a welcome message
connected_socket.sendall(b'What should I yell at you?\n')

# receive a message (up to 4096 bytes)
print('waiting for input')
msg = connected_socket.recv(4096).decode('utf-8')
print('received:')
print(msg)
print()

# send back a message (what we received, but capitalized)
print('sending uppercase version')
connected_socket.sendall(b'\nI\'m going to yell now:\n')
connected_socket.sendall(msg.upper().encode('utf-8'))
connected_socket.sendall(b'\n\n')

# close the connection
connected_socket.close()