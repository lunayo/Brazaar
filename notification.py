from gevent import monkey; monkey.patch_all()
from bottle import *
from bson.json_util import dumps, loads

def collect_data(token=None, elapsed=None) :
	if elapsed :
		fb = open("notification.csv", "a")
		fb.write(str(token) + " " + str(elapsed) + "\n")
		fb.close()

def pre_request(token=None, timestamp=None, timezones=None) :
	current_timestamp = time.time()
	elapsed = int(round((current_timestamp - timestamp) * 1000))
	collect_data(token=token, elapsed=elapsed)
	return

def sendNotification(token=None, content=None) :
	return

@post('/notification/addNotification')
def addNotification() :
	requestBody = loads(request.body.read())
	token = requestBody['token']
	content = requestBody['content']
	timestamp = requestBody['timestamp']
	timezones = requestBody['timezones']
	# pre request
	pre_request(timestamp=timestamp, timezones=timezones, token=token)
	# send notfication to devices
	sendNotification(content=content)
	return

run(host='0.0.0.0', port=8080, debug=True, reloader=True, server="gevent")
# run(host='127.0.0.1', port=8081, debug=True)