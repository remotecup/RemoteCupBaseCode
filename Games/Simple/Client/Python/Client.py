import socket
from Games.Simple.Server.Message import *
from Games.Simple.Client.Python.World import *
import Games.Simple.Client.Python.ClientGreedy as c_greedy
import Games.Simple.Client.Python.ClientRandom as c_random


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    server_address = ('localhost', 20002)
    world = World()
    message_snd = MessageClientConnectRequest(input('enter name:')).build()

    while True:
        sock.sendto(message_snd, server_address)
        try:
            message_rcv = sock.recvfrom(1024)
        except:
            continue
        message = parse(message_rcv[0])
        if message.type == 'MessageClientConnectResponse':
            print('my id is ' + str(message.id))
            world.set_id(message.id, 3)
            break

    while True:
        try:
            r = sock.recvfrom(1024)
        except:
            continue
        message = parse(r[0])
        if message.type == 'MessageClientDisconnect':
            break
        elif message.type == 'MessageClientWorld':
            world.update(message)
            world.print()

            if world.self_id == 1:
                action = c_greedy.get_action(world)
            else:
                action = c_random.get_action(world)
            # action = input('enter:')

            sock.sendto(MessageClientAction(string_action=action).build(), server_address)

