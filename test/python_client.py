#!/usr/bin/env python
import sys
sys.path.append('./gen-py')

from tutorial import UserManager
from tutorial.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

def main():
    # Make socket
    transport = TSocket.TSocket('localhost', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = UserManager.Client(protocol)

    # Connect!
    transport.open()

    client.ping()
    global_id = 1

    while (True):
        com = raw_input('Input command: ')
        if com == 'Add':
            u = User()
            u.user_id = global_id
            u.firstname = raw_input('Input firstname: ')
            u.lastname = raw_input('Input lastname: ')
            sex_type = int(raw_input('Input sex type (1 - Male, 2 - Female): '))
            if sex_type == 1: u.sex = SexType.MALE
            else: u.sex = SexType.FEMALE
            desc = raw_input('Input description (optional): ')
            if len(desc) > 0: u.description = desc
            if client.add_user(u):
                global_id += 1
                print 'user added seccesfully'
            #client.clear_list()
        elif com == 'Info':
            for user in client.get_all_users():
                print 'ID(' + str(user.user_id) + ') Name: ' + user.firstname + ' ' + user.lastname
                print 'SexType: ' + str(user.sex)
                if user.description != None:
                    print 'Description: ' + user.description
        elif com == 'Exit':
            break

    # Close
    transport.close()

if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print('%s' % tx.error_msg)
