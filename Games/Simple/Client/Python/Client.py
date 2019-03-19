import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 20002)

a = {'message_type': 'connect', 'value': {'name': input()}}
sock.sendto(str.encode(str(a)), server_address)
r = sock.recvfrom(1024)
print(str(r[0].decode("utf-8")))
while True:
    r = sock.recvfrom(1024)
    print(str(r[0].decode("utf-8")))
    a = {'message_type': 'action', 'value': {'name': input()}}
    sock.sendto(str.encode(str(a)), server_address)

