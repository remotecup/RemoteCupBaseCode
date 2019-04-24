import socket
import random
from argparse import ArgumentParser
from Base.Message import *
from Games.Soccer.Client.Python.World import *
import Games.Soccer.Client.Python.main_player as main
import signal
is_run = True


def signal_handler(sig, frame):
    global is_run
    print('You pressed Ctrl+C!')
    is_run = False


signal.signal(signal.SIGINT, signal_handler)


def run():
    parser = ArgumentParser()
    parser.add_argument("-n", "--name", dest="name", type=str, default='team_name' + str(random.randint(0, 10000)),
                        help="Client Name", metavar="NAME")
    parser.add_argument("-c", "--client", dest="client_type", type=str, default='auto',
                        help="greedy, random, hand, auto", metavar="ClientType")
    args = parser.parse_args()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    server_address = ('localhost', 20002)
    world = World()
    message_snd = MessageClientConnectRequest(args.name).build()

    while is_run:
        sock.sendto(message_snd, server_address)
        try:
            message_rcv = sock.recvfrom(4096)
        except:
            continue
        message = parse(message_rcv[0])
        if message.type == 'MessageClientConnectResponse':
            print('my id is ' + str(message.id))
            world.set_id(message.id)
            break

    while is_run:
        try:
            r = sock.recvfrom(4096)
        except:
            continue
        message = parse(r[0])
        if message.type == 'MessageClientDisconnect':
            break
        elif message.type == 'MessageClientWorld':
            world.update(message)
            # world.print()

            action = main.get_action(world)
            # check_action_side(actoin,)

            sock.sendto(MessageClientAction(string_action=action).build(), server_address)
            world.clear()

