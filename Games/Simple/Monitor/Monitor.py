import socket
from Games.Simple.Server.Message import *


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('localhost', 20003)

    message_snd = MessageMonitorConnectRequest().build()
    while True:
        sock.sendto(message_snd, server_address)
        r = sock.recvfrom(1024)
        print(r)
        message_rcv = parse(r[0])
        if message_rcv.type is 'MessageMonitorConnectResponse':
            print()
            break
    while True:
        r = sock.recvfrom(1024)
        message = parse(r[0])
        print('cycle: {}'.format(message.cycle))
        world = message.world
        for f in world:
            print(f)
        print('------------------------------------')