#include <thrift/concurrency/ThreadManager.h>
#include <thrift/concurrency/PlatformThreadFactory.h>
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/server/TSimpleServer.h>
#include <thrift/server/TThreadPoolServer.h>
#include <thrift/server/TThreadedServer.h>
#include <thrift/transport/TServerSocket.h>
#include <thrift/transport/TSocket.h>
#include <thrift/transport/TTransportUtils.h>
#include <thrift/TToString.h>

#include <boost/make_shared.hpp>

#include <iostream>
#include <stdexcept>
#include <sstream>

#include "./gen-cpp/AddService.h"

using namespace std;
using namespace apache::thrift;
using namespace apache::thrift::concurrency;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;
using namespace apache::thrift::server;

using namespace calc;

class CalculatorHandler {
public:
  CalculatorHandler() {}

  int32_t add(const int32_t n1, const int32_t n2) {
    cout << "add(" << n1 << ", " << n2 << ")" << endl;
    return n1 + n2;
  }

};

class CalculatorCloneFactory {
 public:
  virtual ~CalculatorCloneFactory() {}
  virtual CalculatorIf* getHandler(const ::apache::thrift::TConnectionInfo& connInfo)
  {
    boost::shared_ptr<TSocket> sock = boost::dynamic_pointer_cast<TSocket>(connInfo.transport);
    cout << "Incoming connection\n";
    cout << "\tSocketInfo: "  << sock->getSocketInfo() << "\n";
    cout << "\tPeerHost: "    << sock->getPeerHost() << "\n";
    cout << "\tPeerAddress: " << sock->getPeerAddress() << "\n";
    cout << "\tPeerPort: "    << sock->getPeerPort() << "\n";
    return new CalculatorHandler;
  }
  virtual void releaseHandler( ::calc::SharedServiceIf* handler) {
    delete handler;
  }
};

int main() {
  TThreadedServer server(
    boost::make_shared<CalculatorProcessorFactory>(boost::make_shared<CalculatorCloneFactory>()),
    boost::make_shared<TServerSocket>(9090), //port
    boost::make_shared<TBufferedTransportFactory>(),
    boost::make_shared<TBinaryProtocolFactory>());

  cout << "Starting the server..." << endl;
  server.serve();
  cout << "Done." << endl;
  return 0;
}
