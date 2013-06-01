__author__ = 'Emmanouil Samatas'

import pymongo
from gevent import monkey; monkey.patch_all()
from bottle import *
from bson.json_util import dumps, loads

connectionString = "ec2-54-228-18-198.eu-west-1.compute.amazonaws.com:27017"

@hook('after_request')
def setHeaders():
    response.content_type = "application/json"


@route('/')
def index():
    connection = pymongo.MongoClient(connectionString)
    db = connection.test
    collection = db.test
    return str(collection.find_one())


@post('/product/getNearbyProducts')
def getNearbyProducts():
    requestBody = loads(request.body.read())
    token = requestBody['token']
    location = requestBody['location']
    try :
        connection = pymongo.MongoClient(connectionString)
        db = connection.brazaar2
        products = db.products
        query = {'location': {'$nearSphere':{
                                '$geometry': { 'type' : 'Point' ,
                                                'coordinates' : [location['long'],location['lat']]}}}}

        nearestProducts = products.find(query).limit(10)
        print nearestProducts
        return dumps(nearestProducts)
    except pymongo.errors.PyMongoError as e :
        response.status = "500 crap"
        return {'error': 'Retrieve Error : ' + str(e)}

@post('/product/addProduct')
def addProduct():
    requestBody = loads(request.body.read())
    token = requestBody['token']
    product = requestBody['product']
    if  not product['quantity']:
        product['quantity'] = 1

    try:
        connection = pymongo.MongoClient(connectionString)
        db = connection.brazaar2
        products = db.products
        products.insert(dict(product))
        return product

    except pymongo.errors.PyMongoError as e:
        response.status = "500 crap"
        return {'error': 'Insert Error : ' + str(e)}


# run(host='ec2-54-228-18-198.eu-west-1.compute.amazonaws.com', port=8000, debug=True, reloader=True, server="gevent")
run(host='127.0.0.1', port=8082, debug=True, reloader=True, server="gevent")
