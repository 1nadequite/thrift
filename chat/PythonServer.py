#!/usr/bin/env python
import glob
import sys
import datetime
sys.path.append('gen-py')

from tutorial import Message

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class MessageHandler:
    def __init__(self):
        self.log = {}

    def print_msg(self, msg):
        now = datetime.datetime.now()
        print('[%d:%d:%d] : %s' % (now.hour, now.minute, now.second, msg))
        return msg

if __name__ == '__main__':
    handler = MessageHandler()

    processor = Message.Processor(handler)
    transport = TSocket.TServerSocket(port = 9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    print('Starting the server...')
    server.serve()
    print('done.')
