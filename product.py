__author__ = 'Emmanouil Samatas'

from gevent import monkey; monkey.patch_all()

from bottle import *
from bson.json_util import dumps, loads

import database

@hook('after_request')
def setHeaders():
    response.content_type = "application/json"


@route('/')
def index():
    return str(database.find_one(database="test", collection="test"))


@post('/product/getNearbyProducts')
def getNearbyProducts():
    requestBody = loads(request.body.read())
    token = requestBody['token']
    location = requestBody['location']
    query = {'location': {'$nearSphere':{
                                        '$geometry': { 'type' : 'Point' ,
                                                       'coordinates' : [location['longitude'],location['latitude']]}}}}

    nearestProducts = database.find(database="brazaar2", 
                                    collection="products",
                                    limit=10)

    if nearestProducts :
        return dumps(nearestProducts)
    else :
        response.status = 300
        return {'error': 'request collection error'}

def uploadImages(folderName, files) :
    for key in files.keys() :
        fileItem = files[key]
        # Test if the file was uploaded
        if fileItem.filename:
            key_name = folderName + '/' + fileItem.filename
            database.upload_image(key_name=key_name, bucket="brazaar",
                                 data=fileItem.file)
            message = 'The file "' + fileItem.filename + '" was uploaded successfully'
        else:
            message = 'No file was uploaded'

        print message

@post('/product/addProduct')
def addProduct():

    requestBody = request.forms
    token = requestBody['token']
    productRequest = {}
    product = {}
    product['name'] = requestBody['product[name]']
    product['location'] = [requestBody['product[location][longitude]'],requestBody['product[location][latitude]']]
    product['description'] = requestBody['product[description]']
    product.setdefault('quantity', 1)
    productRequest['token'] = token
    productRequest['product'] = product

    productID = database.insert(database="brazaar2", 
                                collection="products",
                                data=dict(productRequest))

    if productID :
        t1 = threading.Thread(target=uploadImages,args=(str(productID), request.files))
        t1.start()
        return dumps(product)
    else :
        response.status = 300
        return {'error': 'insert to collection error'}

@post('/user/addFollower')
def addFollower():
    relationship = {}
    session = {'username':"samatase"}
    requestBody = loads(request.body.read())
    token = requestBody['token']
    relationship['following'] = requestBody['username']
    relationship['user'] = session['username']

    userQuery = '{"username":' + relationship['following'] + '}'
    validate = list(database.find(database="brazaar2", 
                                 collection="users",
                                 query=userQuery))

    if validate :
        relationshipID = database.insert(database="brazaar2", 
                                        collection="relationships",
                                        data=dict(relationship))
        return dumps(relationship)
    else :
        response.status = 300
        return {'error': 'Invalid username'}

@post ('/user/createUser')
def createUser():
    user = {}
    requestBody = loads(request.body.read())
    token = requestBody['token']
    user['username'] = requestBody['username']
    user['firstName'] = requestBody['firstName']
    user['lastName'] = requestBody['lastName']

    userID = database.insert(database="brazaar2", 
                            collection="users",
                            data=dict(user))
        
    if userID :
        return dumps(user)
    else :
        response.status = 300
        return {'error': 'insert to collection error'}

@get ('/user/getFollowings')
def getFollowing():
    session = {'username':"samatase"}
    followingUsers = []
    requestBody = loads(request.body.read())
    user = session['username']

    followingsQuery = '{"user":user},{"following":1,"_id":0}'
    followings = list(database.find(database="brazaar2", 
                                    collection="relationships",
                                    query=followingsQuery))

    usersQuery = '{"username":' + following['following'] + '},{"firstName":1,"lastName":1,"_id":0}'
    for following in followings:
        user = database.find(database="brazaar2", 
                            collection="users",
                            query=usersQuery,
                            limit=1)
        if user :
            followingUsers.append(list(user))
        else :
            return {'error' : 'invalid user'}

    return dumps(followingUsers)

run(host='0.0.0.0', port=8080, debug=True, reloader=True, server="gevent")
# run(host='127.0.0.1', port=8082, debug=True)