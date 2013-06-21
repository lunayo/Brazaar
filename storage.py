from boto.s3.connection import S3Connection
from boto.s3.connection import Location
from boto.s3.connection import Key
import sys,os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import haproxy_autoscale.amazon_key

class kUploadContentType:
    File, FileName, String, Stream = range(4)

def get_connection() :
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

