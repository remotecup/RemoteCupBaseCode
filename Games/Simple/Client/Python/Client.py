import socket
import random
from Games.Simple.Server.Message import *

def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('localhost', 20002)
    message_snd = MessageClientConnectRequest(input('enter name:')).build()
    while True:
        sock.sendto(message_snd, server_address)
        message_rcv = sock.recvfrom(1024)
        message = parse(message_rcv[0])
        if message.type == 'MessageClientConnectResponse':
            print('my id is ' + str(message.id))
            my_id = message.id
            break
    while True:
        r = sock.recvfrom(1024)
        message = parse(r[0])
        print('cycle: {}'.format(message.cycle))
        world = message.world
        for f in world:
            print(f)
        print('------------------------------------')

        if my_id == 1:
            my_pos = [0, 0]
            for i in range(len(world)):
                for j in range(len(world[i])):
                    if world[i][j] == my_id:
                        my_pos = [i, j]
            goal_pos = [0, 0]
            for i in range(len(world)):
                for j in range(len(world[i])):
                    if world[i][j] == 3:
                        goal_pos = [i, j]
            if goal_pos[0] > my_pos[0]:
                action = 'd'
            elif goal_pos[0] < my_pos[0]:
                action = 'u'
            elif goal_pos[1] > my_pos[1]:
                action = 'r'
            elif goal_pos[1] < my_pos[1]:
                action = 'l'
        else:
            actions = ['u', 'd', 'l', 'r']
            action = actions[random.randint(0, 3)]
        # action = input('enter:')
        
        sock.sendto(MessageClientAction(string_action=action).build(), server_address)

