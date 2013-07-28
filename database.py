import pymongo
import storage

connectionString = "127.0.0.1:27017"
connection = None

def get_connection() :
    global connection
    if not connection :
        try :
            connection = pymongo.MongoClient(connectionString)
        except pymongo.errors.PyMongoError as e:
            print "Connection Error: " + str(e)
    return connection

def get_collection(database=None, collection=None) :
    try :
        conn = get_connection()
        db = conn[database]
    except pymongo.errors.PyMongoError as e:
        print "Get Collection Error: " + str(e)
    return db[collection]

def pre_data() :
    return None


# process related to database 
def find_one(database=None, collection=None) :
    pre_data()
    collection = get_collection(database, collection)
    return collection.find_one()

def find(database=None, collection=None, query=None, limit=0) :
    pre_data()
    collection = get_collection(database, collection)
    return collection.find(query).limit(limit)

def insert(database=None, collection=None, data=None) :
    pre_data()
    try :
        collection = get_collection(database, collection)
    except pymongo.errors.PyMongoError as e:
        print "Insert to Collection Error: " + str(e)
    return collection.insert(data)

# process related to the file system storage
def upload_image(bucket=None, key_name=None, data=None) :
    return storage.upload_content(bucket=bucket, key_name=key_name,
                                    data_type=storage.kUploadContentType.File,
                                    data=data)

def get_images(bucket=None, key_name=None) :
    return storage.retrieve_content(bucket=bucket, key_name=key_name)



