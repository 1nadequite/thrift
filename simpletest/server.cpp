#include "gen-cpp/Calculator.h"
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/server/TSimpleServer.h>
#include <thrift/transport/TServerSocket.h>
#include <thrift/transport/TBufferTransports.h>

using namespace ::apache::thrift;
using namespace ::apache::thrift::protocol;
using namespace ::apache::thrift::transport;
using namespace ::apache::thrift::server;

using boost::shared_ptr;

class CalculatorHandler : virtual public CalculatorIf {
 public:
  int32_t add(const int32_t a, const int32_t b) override { return a + b; }
  int32_t sub(const int32_t a, const int32_t b) override { return a - b; }
  int32_t mult(const int32_t a, const int32_t b) override { return a * b; }
  int32_t div(const int32_t a, const int32_t b) override { return a / b; }
};

int main(int argc, char **argv) {
  int port = 10000;
  shared_ptr<CalculatorHandler> handler(new CalculatorHandler());
  shared_ptr<TProcessor> processor(new CalculatorProcessor(handler));
  shared_ptr<TServerTransport> serverTransport(new TServerSocket(port));
  shared_ptr<TTransportFactory> transportFactory(new TBufferedTransportFactory());
  shared_ptr<TProtocolFactory> protocolFactory(new TBinaryProtocolFactory());

  TSimpleServer server(processor, serverTransport, transportFactory, protocolFactory);
  server.serve();
  return 0;
}

