#!/usr/bin/env python
import sys
import datetime
sys.path.append('./gen-py')

from tutorial import UserManager
from tutorial.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

def date_to_str(now):
    cur_time = str(now.hour) + ':' + str(now.minute) + ':' + str(now.second)
    return cur_time

def main():
    # Make socket
    transport = TSocket.TSocket('localhost', 9080)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = UserManager.Client(protocol)

    # Connect!
    transport.open()

    # client.ping()
    global_user_id = 1
    while (True):
        nick = raw_input("Input your nickname: ")
        if client.user_connect(nick):
            print "Welcome to main chat."
            print "Print '/command' for more information"
            break

    while (True):
        com = raw_input()
        '''if com == 'Add':
            u = User()
            u.user_id = global_user_id
            u.nickname = nick
            u.firstname = raw_input('Input firstname: ')
            u.lastname = raw_input('Input lastname: ')
            sex_type = int(raw_input('Input sex type (1 - Male, 2 - Female): '))
            if sex_type == 1: u.sex = SexType.MALE
            else: u.sex = SexType.FEMALE
            desc = raw_input('Input description (optional): ')
            if len(desc) > 0: u.description = desc
            if client.add_user(u):
                global_user_id += 1
                print 'user added seccesfully'
        '''
        if com == '/command':

        elif com == '/users':
            print 'Users online: '
            for user in client.get_all_users():
                print user
        elif com == '/message':
            for msg in client.last_messages():
                print '[%s] : %s said' % (msg.date, msg.user)
                print msg.text
        elif com == '/exit':
            client.user_disconnect(nick)
            break
        else:
            msg = Message()
            now = datetime.datetime.now()
            msg.date = date_to_str(now)
            msg.user = nick
            msg.text = com
            client.print_message(msg)

    # Close
    transport.close()

if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print('%s' % tx.error_msg)
