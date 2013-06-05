__author__ = 'Emmanouil Samatas'

import pymongo
#from gevent import monkey; monkey.patch_all()
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
                                                           'coordinates' : [location['longitude'],location['latitude']]}}}}

        nearestProducts = products.find(query).limit(10)
        return dumps(nearestProducts)
    except pymongo.errors.PyMongoError as e:
        response.status = 300
        return {'error': 'Find Error : ' + str(e)}

@post('/product/addProduct')
def addProduct():

    requestBody = request.forms
    token = requestBody['token']
    product = {}
    product['name'] = requestBody['product[name]']
    product['location'] = [requestBody['product[location][longitude]'],requestBody['product[location][latitude]']]
    product['description'] = requestBody['product[description]']
    product.setdefault('quantity', 1)

    try:
        connection = pymongo.MongoClient(connectionString)
        db = connection.brazaar2
        products = db.products
        productID = products.insert(dict(product))

        for key in request.files.keys() :
        fileitem = request.files[key]
        # Test if the file was uploaded
        if fileitem.filename:
           # strip leading path from file name to avoid directory traversal attacks
           fn = os.path.basename(fileitem.filename)
           open(os.getcwd() + '/Images/' + fn, 'wb').write(fileitem.file.read())
           message = 'The file "' + fn + '" was uploaded successfully'
        else:
           message = 'No file was uploaded'

        print message

        return product

    except pymongo.errors.PyMongoError as e:
        response.status = 300
        return {'error': 'Insert Error : ' + str(e)}
    else :
        response.status = 300
        return {'error': 'Image Error : ' + str(e)}

@post('/user/addFollower')
def addFollower():
    relationship = {}
    session = {'username':"samatase"}
    requestBody = loads(request.body.read())
    token = requestBody['token']
    relationship['following'] = requestBody['username']
    relationship['user'] = session['username']

    try:
        connection = pymongo.MongoClient(connectionString)
        db = connection.brazaar2

        relationships = db.relationships

        validate = list(db.users.find({"username":relationship['following']}))


        if validate:
            relationships.insert(dict(relationship))
            return relationship
        else:
            response.status = 300
            return 'Invalid username'

    except pymongo.errors.PyMongoError as e:
        response.status = 300
        return {'error': 'Insert Error : ' + str(e)}

@post('/user/addFollower')
def addFollower():
    relationship = {}
    session = {'username':"samatase"}
    requestBody = loads(request.body.read())
    token = requestBody['token']
    relationship['following'] = requestBody['username']
    relationship['user'] = session['username']

    try:
        connection = pymongo.MongoClient(connectionString)
        db = connection.brazaar2

        relationships = db.relationships

        validate = list(db.users.find({"username":relationship['following']}))


        if validate:
            relationships.insert(dict(relationship))
            return relationship
        else:
            response.status = 300
            return 'Invalid username'

    except pymongo.errors.PyMongoError as e:
        response.status = 300
        return {'error': 'Insert Error : ' + str(e)}

@post ('/user/createUser')
def createUser():
    user = {}
    requestBody = loads(request.body.read())
    token = requestBody['token']
    user['username'] = requestBody['username']
    user['firstName'] = requestBody['firstName']
    user['lastName'] = requestBody['lastName']


    try:
        connection = pymongo.MongoClient(connectionString)
        db = connection.brazaar2
        users = db.users
        users.insert(user)
    except pymongo.errors.PyMongoError as e:
        response.status = 300
        return {'error': 'Insert Error : ' + str(e)}

@get ('/user/getFollowings')
def getFollowing():
    session = {'username':"samatase"}
    followingUsers = []
    requestBody = loads(request.body.read())
    user = session['username']

    try:
        connection = pymongo.MongoClient(connectionString)
        db = connection.brazaar2
        followings = list(db.relationships.find({"user":user},{"following":1,"_id":0}))
        for following in followings:
            followingUsers.append(list(db.users.find({"username":following['following']},{"firstName":1,"lastName":1,"_id":0}).limit(1)))
        return dumps(followingUsers)
    except pymongo.errors.PyMongoError as e:
        response.status = 300
        return {'error': 'Connection Error : ' + str(e)}

# run(host='ec2-54-228-18-198.eu-west-1.compute.amazonaws.com', port=8000, debug=True, reloader=True, server="gevent")
run(host='127.0.0.1', port=8082, debug=True, reloader=True)
