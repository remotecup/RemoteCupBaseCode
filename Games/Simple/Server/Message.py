from Games.Simple.Server.Math import *


class Message:
    def __init__(self):
        self.type = 'Message'
        pass

    def build(self):
        pass

    @staticmethod
    def parse(self):
        pass


class MessageClientConnectRequest(Message):
    def __init__(self, name='sample_client'):
        self.type = "ClientConnectRequest"
        self.client_name = name

    def build(self):
        msg = {"message_type": self.type, "value": {"name": self.client_name}}
        str_msg = str.encode(str(msg))
        return str_msg

    @staticmethod
    def parse(coded_msg):
        msg = eval(str(coded_msg.decode("utf-8")))
        if msg['message_type'] == "ClientConnectRequest":
            message = MessageClientConnectRequest(msg['value']['name'])
            return True, message
        return False, None


class MessageClientConnectResponse(Message):
    def __init__(self, id):
        self.type = "MessageClientConnectResponse"
        self.id = id

    def build(self):
        msg = {"message_type": self.type, "value": {"id": self.id}}
        str_msg = str.encode(str(msg))
        return str_msg

    @staticmethod
    def parse(coded_msg):
        msg = eval(str(coded_msg.decode("utf-8")))
        if msg['message_type'] == "MessageClientConnectResponse":
            message = MessageClientConnectResponse(msg['value']['id'])
            return True, message
        return False, None


class MessageClientDisconnect(Message):
    def __init__(self):
        self.type = "MessageClientDisconnect"

    def build(self):
        msg = {"message_type": self.type, "value": {}}
        str_msg = str.encode(str(msg))
        return str_msg

    @staticmethod
    def parse(coded_msg):
        msg = eval(str(coded_msg.decode("utf-8")))
        if msg['message_type'] == "MessageClientDisconnect":
            message = MessageClientDisconnect()
            return True, message
        return False, None


class MessageMonitorConnectRequest(Message):
    def __init__(self):
        self.type = "MessageMonitorConnectRequest"

    def build(self):
        msg = {"message_type": self.type, "value": {}}
        str_msg = str.encode(str(msg))
        return str_msg

    @staticmethod
    def parse(coded_msg):
        msg = eval(str(coded_msg.decode("utf-8")))
        if msg['message_type'] == "MessageMonitorConnectRequest":
            message = MessageMonitorConnectRequest()
            return True, message
        return False, None


class MessageMonitorConnectResponse(Message):
    def __init__(self):
        self.type = "MessageMonitorConnectResponse"

    def build(self):
        msg = {"message_type": self.type, "value": {}}
        str_msg = str.encode(str(msg))
        return str_msg

    @staticmethod
    def parse(coded_msg):
        msg = eval(str(coded_msg.decode("utf-8")))
        if msg['message_type'] == "MessageMonitorConnectResponse":
            message = MessageMonitorConnectResponse()
            return True, message
        return False, None


class MessageClientWorld(Message):
    def __init__(self, cycle, board, score):
        self.type = "MessageClientWorld"
        self.cycle = cycle
        self.board = board
        self.score = score

    def build(self):
        msg = {"message_type": self.type, "value": {"cycle": self.cycle, "score": self.score, "board": self.board}}
        str_msg = str.encode(str(msg))
        return str_msg

    @staticmethod
    def parse(coded_msg):
        msg = eval(str(coded_msg.decode("utf-8")))
        if msg['message_type'] == "MessageClientWorld":
            cycle = msg['value']['cycle']
            world = msg['value']['board']
            score = msg['value']['score']
            message = MessageClientWorld(cycle, world, score)
            return True, message
        return False, None


class MessageClientAction(Message):
    def __init__(self, vector_action=Vector2D(0, 0), string_action=''):
        self.type = "MessageClientAction"
        self.vector_action = vector_action
        self.string_action = string_action

    def build(self):
        msg = {"message_type": self.type, "value": {"action": self.string_action}}
        str_msg = str.encode(str(msg))
        return str_msg

    @staticmethod
    def parse(coded_msg):
        msg = eval(str(coded_msg.decode("utf-8")))
        if msg['message_type'] == "MessageClientAction":
            string_action = msg['value']['action']
            if string_action is 'u':
                action = Vector2D(-1, 0)
            elif string_action is 'd':
                action = Vector2D(1, 0)
            elif string_action is 'l':
                action = Vector2D(0, -1)
            elif string_action is 'r':
                action = Vector2D(0, 1)
            else:
                action = None
            message = MessageClientAction(vector_action=action)
            return True, message
        return False, None


def parse(coded_msg):
    ret = MessageClientConnectRequest.parse(coded_msg)
    if ret[0]:
        return ret[1]

    ret = MessageClientConnectResponse.parse(coded_msg)
    if ret[0]:
        return ret[1]

    ret = MessageClientDisconnect.parse(coded_msg)
    if ret[0]:
        return ret[1]

    ret = MessageMonitorConnectRequest.parse(coded_msg)
    if ret[0]:
        return ret[1]

    ret = MessageMonitorConnectResponse.parse(coded_msg)
    if ret[0]:
        return ret[1]

    ret = MessageClientAction.parse(coded_msg)
    if ret[0]:
        return ret[1]

    ret = MessageClientWorld.parse(coded_msg)
    if ret[0]:
        return ret[1]

    return Message()
