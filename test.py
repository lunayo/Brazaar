
__author__ = 'Emmanouil Samatas'

import pymongo
import bottle

@bottle.route('/')
def index():
    connection = pymongo.MongoClient("mongodb://localhost")
    db = connection.test
    collection = db.test
    collection.insert({"test":"Hello"})
    return str(collection.find_one())


bottle.run(host='localhost', port=8082, debug=True)