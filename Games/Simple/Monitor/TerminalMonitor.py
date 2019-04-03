import socket
from Games.Simple.Server.Message import *


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('localhost', 20003)

    message_snd = MessageMonitorConnectRequest().build()
    while True:
        sock.sendto(message_snd, server_address)
        r = sock.recvfrom(4096)
        message_rcv = parse(r[0])
        if message_rcv.type is 'MessageMonitorConnectResponse':
            break
    while True:
        r = sock.recvfrom(4096)
        message = parse(r[0])
        if message.type == 'MessageClientDisconnect':
            break
        print('cycle: {}'.format(message.cycle))
        print('score: {}'.format(str(message.score)))
        board = message.board
        for f in board:
            print(f)
        print('------------------------------------')