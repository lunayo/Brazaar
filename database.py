import pymongo
import storage

connectionString = "127.0.0.1:27017"

def get_connection() :
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

def pre_retrieve_data() :
    return None

def pre_insert_data() :
    return None

# process related to database 
def find_one(database=None, collection=None) :
    collection = get_collection(database, collection)
    return collection.find_one()

def find(database=None, collection=None, query=None, limit=0) :
    collection = get_collection(database, collection)
    return collection.find(query).limit(limit)

def insert(database=None, collection=None, data=None) :
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



