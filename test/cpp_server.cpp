#include "./gen-cpp/UserManager.h"
#include <stdint.h>
#include <concurrency/ThreadManager.h>
#include <concurrency/PosixThreadFactory.h>
#include <protocol/TBinaryProtocol.h>
#include <server/TSimpleServer.h>
#include <server/TThreadPoolServer.h>
#include <server/TThreadedServer.h>
#include <server/TNonblockingServer.h>
#include <transport/TServerSocket.h>
#include <transport/TTransportUtils.h>

#include <iostream>
#include <vector>

using namespace apache::thrift;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;
using namespace apache::thrift::server;
using namespace apache::thrift::concurrency;

using boost::shared_ptr;

using namespace std;
using namespace tutorial;

class UserManagerHandler  {
public:
  UserManagerHandler() {}

  void ping() {
    cout << "ping()" << endl;
  }

  uint32_t add_user(const User& u) {
    /*if (!u.firstname) {
      InvalidValueException err;
      err.error_code = 1;
      err.error_msg = "No firstname exception";
      throw err;
    }
    if (u.lastname == NULL)
      throw InvalidValueException("No lastname exception");
    if (u.user_id <= 0)
      throw InvalidValueException("Wrong user id");
    if (u.sex != SexType::MALE && u.sex != SexType::FEMALE)
      throw InvalidValueException("Wrong sex id");*/
    cout << "Processing user " << u.firstname << ' ' << u.lastname << endl;
    users.push_back(u);
    return 1;
  }

  User get_user(const uint32_t user_id) {
    /*if (user_id < 0)
      throw InvalidValueException("Wrong id"); */
    return users[user_id];
  }

  vector<User> get_all_users() {
    /*if (users.size() == 0)
      throw InvalidValueException("List is empty");*/
    cout << "All added users" << endl;
    /*for (auto& u: users) {
      cout << "[ " << u.firstname << ' ' << u.lastname << " ]" << endl;
    }*/
    return users;
  }

  void clear_list() {
    cout << "Clearing list" << endl;
    users.clear();
  }

protected:
  vector<User> users;
};

int main() {
  /*shared_ptr<UserManagerHandler> handler(new UserManagerHandler());
  shared_ptr<TProcessor> processor(new UserManagerProcessor(handler));
  shared_ptr<TServerTransport> serverTransport(new TServerSocket(9090));
  shared_ptr<TTransportFactory> transportFactory(new TBufferedTransportFactory());
  shared_ptr<TProtocolFactory> protocolFactory(new TBinaryProtocolFactory());

  TSimpleServer server(processor, serverTransport, transportFactory, protocolFactory);

  // using thread pool with maximum 15 threads to handle incoming requests
  shared_ptr<ThreadManager> threadManager = ThreadManager::newSimpleThreadManager(15);
  shared_ptr<PosixThreadFactory> threadFactory = shared_ptr<PosixThreadFactory>(new PosixThreadFactory());
  threadManager->threadFactory(threadFactory);
  threadManager->start();
  TNonblockingServer server(processor, protocolFactory, 8888, threadManager);
  */

  shared_ptr<TProtocolFactory> protocolFactory(new TBinaryProtocolFactory());
  shared_ptr<UserManagerHandler> handler(new UserManagerHandler());
  shared_ptr<TProcessor> processor(new UserManagerProcessor(handler));

  shared_ptr<ThreadManager> threadManager = ThreadManager::newSimpleThreadManager(15);
  shared_ptr<PosixThreadFactory> threadFactory = shared_ptr<PosixThreadFactory>(new PosixThreadFactory());
  threadManager->threadFactory(threadFactory);
  threadManager->start();

  TNonblockingServer server(processor, protocolFactory, 9090, threadManager);

  cout << "Starting the server..." << endl;
  server.serve();
  cout << "done." << endl;

  return 0;
}
