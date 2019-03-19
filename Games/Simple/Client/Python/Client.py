import socket
import random
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 20002)

a = {'message_type': 'connect', 'value': {'name': input('enter name:')}}
sock.sendto(str.encode(str(a)), server_address)
r = sock.recvfrom(1024)
print(str(r[0].decode("utf-8")))
r = sock.recvfrom(1024)
print('my id is ' + str(r[0].decode("utf-8")))
my_id = int(r[0].decode("utf-8"))
while True:
    r = sock.recvfrom(1024)
    world = eval(r[0].decode("utf-8"))
    print(world)
    print(type(world[0][0]))
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
        action = actions[random.randint(0,3)]
    a = {'message_type': 'action', 'value': {'name': action}}
    sock.sendto(str.encode(str(a)), server_address)

