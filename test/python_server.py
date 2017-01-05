import sys
import datetime
sys.path.append('./gen-py')

from tutorial import UserManager
from tutorial.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

users = []
messages = []

class UserManagerHandler:
    def __init__(self):
        pass
        #self.log = {}

    def ping(self):
        print 'ping()'

    def user_connect(self, user):
        if user in users:
            return False
        else:
            print 'User ' + user + ' connects to main chat.'
            users.append(user)
            return True

    def user_disconnect(self, user):
        users.remove(user)
        print 'User ' + user + ' leaves from the chat.'

    def get_all_users(self):
        return users

    def last_messages(self):
        if len(messages) == 0:
            raise InvalidValueException(7, 'Chat is empty.')
        idx = min(5, len(messages)) * -1
        return messages[idx:]

    def print_message(self, msg):
        messages.append(msg)
        print('[%s] : %s says' % (msg.date, msg.user))
        print msg.text

handler = UserManagerHandler()
processor = UserManager.Processor(handler)
transport = TSocket.TServerSocket(port = 9080)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

#server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
#server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

print 'Starting the server...'
server.serve()
print 'done.'

