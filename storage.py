from boto.s3.connection import S3Connection
from boto.s3.connection import Location
from boto.s3.connection import Key
import sys,os.path
import tempfile
import base64
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from haproxy_autoscale import amazon_key

connection = None

class kUploadContentType:
    File, FileName, String, Stream = range(4)

def get_connection() :
    global connection
    if not connection :
        try :
            connection = S3Connection(aws_access_key_id=amazon_key.ACCESS_KEY, 
                                    aws_secret_access_key=amazon_key.SECRET_KEY)
        except Exception, e :
            print "Connetion to S3 error " + str(e)
    return connection

def get_bucket(bucket=None) :
    conn = get_connection()
    bucket = conn.get_bucket(bucket)
    return bucket

def pre_upload_content() :
    return None

def pre_retrieve_content() :
    return None

def delete_contents(bucket=None, exception="") :
    bucket = get_bucket(bucket)
    bucket_list = bucket.list()
    bucket.delete_keys([key.name for key in bucket_list if key.name.find(exception)])

def upload_content(bucket=None, key_name=None, 
                    data_type=kUploadContentType.String, data=None) :
    bucket = get_bucket(bucket)
    bucketKey = Key(bucket)
    bucketKey.key = key_name
    try :
        if data_type == kUploadContentType.String :
            bucketKey.set_contents_from_string(data)
        elif data_type == kUploadContentType.File :
            bucketKey.set_contents_from_file(data)
        elif data_type == kUploadContentType.FileName(data) :
            bucketKey.set_contents_from_filename(data)
        elif data_type == kUploadContentType.Stream :
            bucketKey.set_contents_from_stream(data)
        return True
    except Exception, e :
        return False

def retrieve_content(bucket=None, key_name=None) :
    images = []
    bucket = get_bucket(bucket)
    bucket_list = bucket.list(key_name)
    for l in bucket_list :
        images.append(base64.b64encode(l.get_contents_as_string()))
    return images

delete_contents(bucket="brazaar", exception="51e6fe718258cd05d1ff6924")
