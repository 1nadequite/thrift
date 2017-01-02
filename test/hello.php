<?php
$GLOBALS['THRIFT_ROOT'] = 'src';

require_once $GLOBALS['THRIFT_ROOT'].'/Thrift.php';
require_once $GLOBALS['THRIFT_ROOT'].'/protocol/TBinaryProtocol.php';
require_once $GLOBALS['THRIFT_ROOT'].'/transport/TSocket.php';
require_once $GLOBALS['THRIFT_ROOT'].'/transport/THttpClient.php';
require_once $GLOBALS['THRIFT_ROOT'].'/transport/TBufferedTransport.php';

require_once $GLOBALS['THRIFT_ROOT'].'/packages/tutorial/UserManager.php';
try {

	$socket = new TSocket('localhost', 9090);
	$transport = new TBufferedTransport($socket, 1024, 1024);
	$protocol = new TBinaryProtocol($transport);
	$client = new UserManagerClient($protocol);

	$transport->open();
	$client->ping();
	$u = new hello_User();
	$u->user_id = 1;
	$u->firstname = 'John';
	$u->lastname = 'Smith';
	$u->sex = hello_SexType::MALE;
	if ($client->add_user($u))
	{
		echo 'user added succesfully</br>';
	}

	var_dump($client->get_user(0));

	$client->clear_list();



	$u2 = new hello_User();
	$client->add_user($u2);

} catch (hello_InvalidValueException $e) {
	echo $e->error_msg.'<br/>';
}

?>
