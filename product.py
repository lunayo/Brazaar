__author__ = 'Emmanouil Samatas'

import pymongo
from bottle import *
from bson.json_util import dumps, loads

connectionString = "mongodb://localhost"

@hook('after_request')
def setHeaders():
    response.content_type = "application/json"


@route('/')
def index():
    connection = pymongo.MongoClient(connectionString)
    connection = pymongo.MongoClient()
    db = connection.test
    collection = db.test
    return str(collection.find_one())


@post('/getNearbyProducts')
def getNearbyProducts():
    requestBody = loads(request.body.read())
    token = requestBody['token']
    location = requestBody['location']
    connection = pymongo.MongoClient(connectionString)
    db = connection.brazaar
    products = db.products
    query = {'location': {'$near': [location['long'], location['lat']]}}

    nearestProducts = products.find(query).limit(10)

    return dumps(nearestProducts)


@post('/addProduct')
def addProduct():
    requestBody = loads(request.body.read())
    token = requestBody['token']
    product = requestBody['product']
    if  not product['quantity']:
        product['quantity'] = 1

    try:
        connection = pymongo.MongoClient(connectionString)
        db = connection.brazaar
        products = db.products
        products.insert(dict(product))
        return product

    except pymongo.errors.PyMongoError as e:
        response.status = "400 crap"
        return {'error': 'Insert Error'}

run(host='localhost', port=8082, debug=True)