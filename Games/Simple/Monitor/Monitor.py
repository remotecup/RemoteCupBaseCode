import socket
import random
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 20003)

a = {'message_type': 'connect_monitor', 'value': {}}
sock.sendto(str.encode(str(a)), server_address)
r = sock.recvfrom(1024)
print(str(r[0].decode("utf-8")))
r = sock.recvfrom(1024)
print('my id is ' + str(r[0].decode("utf-8")))
while True:
    r = sock.recvfrom(1024)
    message = eval(r[0].decode("utf-8"))
    print('cycle: {}'.format(message['value']['cycle']))
    world = message['value']['world']
    for f in world:
        print(f)
    print('------------------------------------')