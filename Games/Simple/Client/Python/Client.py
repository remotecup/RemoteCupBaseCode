import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 20002)

a = {'message_type':'connect', 'value':{'name':'mahtab'}}

sock.sendto(str.encode(str(a)), server_address)
