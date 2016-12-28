#!/usr/bin/env python
import sys
import glob
sys.path.append('gen-py')

from calc import AddService

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
    client = AddService.Client(protocol)

    # Connect!
    transport.open()

    n1 = int(raw_input('1 number: '))
    n2 = int(raw_input('2 number: '))

    sum_ = client.add(n1, n2)
    print('Sum: %d + %d = %d' % (n1, n2, sum_))

    # Close!
    transport.close()

if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print('%s' % tx.message)
