namespace py tutorial

typedef i32 MyInteger

enum SexType {
  MALE = 1,
  FEMALE = 2
}

struct User {
   1: string nickname,
   2: string firstname,
   3: string lastname,
   4: i32 user_id = 0,
   5: SexType sex,
   6: bool active = false,
   7: optional string description
}

struct Message {
  1: string date,
  2: string user,
  3: string text
}

exception InvalidValueException {
  1: i32 error_code,
  2: string error_msg
}

service UserManager {
  void ping(),
  i32 user_connect(1: string u) throws (1: InvalidValueException e),
  i32 user_disconnect(1: string u) throws (1: InvalidValueException e),
  i32 add_user(1: User u) throws (1: InvalidValueException e),
  list<string> get_all_users() throws (1: InvalidValueException e),
  list<Message> last_messages() throws (1: InvalidValueException e),
  void print_message(1: Message m) throws (1: InvalidValueException e),
}
