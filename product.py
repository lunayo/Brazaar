
__author__ = 'Emmanouil Samatas'

import pymongo
from bottle import *
from bson.json_util import dumps , loads
connection = pymongo.MongoClient("mongodb://localhost")
@route('/')
def index():
    connection = pymongo.MongoClient()
    db = connection.test
    collection = db.test
    return str(collection.find_one())

@post('/getNearbyProducts')
def getNearbyProducts():
    requestBody = loads(request.body.read())
    token = requestBody['token']
    location = requestBody['location']

    db = connection.brazaar
    products = db.products
    query = {'location': {'$near':[location['long'],location['lat']]}}

    nearestProducts = products.find(query).limit(10)

    return dumps(nearestProducts)

run(host='localhost', port=8082, debug=True)