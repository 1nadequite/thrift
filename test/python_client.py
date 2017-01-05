#!/usr/bin/env python
import sys
import time, readline, thread
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

def synch_thread():
    while True:
        time.sleep(1)
        sys.stdout.write('\r'+' '*(len(readline.get_line_buffer())+2)+'\r')
        print 'Some text'
        sys.stdout.write(readline.get_line_buffer())
        sys.stdout.flush()

def main():
    transport = TSocket.TSocket('localhost', 9080)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = UserManager.Client(protocol)

    transport.open()

    global_user_id = 1
    while (True):
        nick = raw_input("Input your nickname: ")
        if client.user_connect(nick):
            print "Welcome to main chat."
            print "Print '/command' for more information"
            break

    thread.start_new_thread(synch_thread, ())
    while (True):
        com = raw_input()
        #if com == '/command':
        if com == '/users':
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

    transport.close()

if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print('%s' % tx.error_msg)
