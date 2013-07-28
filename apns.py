import ssl
from bson.json_util import dumps, loads
import socket
import struct
import pprint
import binascii

sock = None
# the certificate file generated from Provisioning Portal
certfile = 'resources/apns-dev.pem'
# APNS server address (use 'gateway.push.apple.com' for production server)
apns_address = ('gateway.sandbox.push.apple.com', 2195)

def open_socket(): 
    global sock
    # create socket and connect to APNS server using SSL
    sock = ssl.wrap_socket( socket.socket( socket.AF_INET, socket.SOCK_STREAM ), certfile = certfile )
    try :
        sock.connect(apns_address)
    except Exception, e:
        print "Connect to apple failed! : ", e

def close_socket():
    global sock
    sock.close()
 
def send_push_message(token, payload):
    global sock
    # generate APNS notification packet
    print payload
    token = token.replace(' ','').decode('hex')
    fmt = '!BH32sH%ds' % len(payload)
    msg = struct.pack(fmt, 0, 32, token, len(payload), payload)
    try :
        sock.write(msg)
    except Exception, e:
        print "Write to socket failed! : ", e

def construct_payload(message=None, badge=1, sound="default"):
    payload = {
        "aps": {
          "alert":message,
          "sound":sound,
          "badge":badge,
        }
     }

    return dumps(payload)

# test send notification
token = "c206ac647b502c461d235352e8240658fe6f25dc2af9ea6345ddb6bf01234c07"
payload = construct_payload(message="Start browsing nearby trending products!")
open_socket()
send_push_message(token=token, payload=payload)
close_socket()




