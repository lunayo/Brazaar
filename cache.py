import memcache

connection_servers = ['ec2-54-217-229-240.eu-west-1.compute.amazonaws.com:11211']
connection = None

def get_connection() :
	global connection
	if not connection :
		connection = memcache.Client(connection_servers, debug=0)
	return connection

def pre_cache() :
	return

def get_cache(key=None) :
	pre_cache()
	conn = get_connection()
	value = conn.get(key)
	return value

def set_cache(key=None, value=None) :
	pre_cache()
	conn = get_connection()
	return conn.set(key, value, 60)

def del_cache(key=None) :
	pre_cache()
	conn = get_connection()
	return conn.delete(key)

