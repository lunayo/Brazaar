__author__ = 'Emmanouil Samatas'

from gevent import monkey; monkey.patch_all()

from bottle import *
from bson.json_util import dumps, loads
from cStringIO import StringIO
from datetime import datetime
from time import gmtime, strftime
import random, string
import time
import gevent
import requests
import database
import cache
import apns
import base64

@hook('after_request')
def setHeaders():
    response.content_type = "application/json"

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

@route('/')
def index():
    return str(database.find_one(database="test", collection="test"))

def sendNotification(token=None, content=None) :
    # build connection with notification servers

    url = "http://ec2-54-217-229-240.eu-west-1.compute.amazonaws.com:8080/notification/addNotification"
    timestamp = time.time()
    timezones = strftime("%z", gmtime())
    payload = {'token':token,
                'content':content,
                'timestamp':timestamp,
                'timezones':timezones}

    greenlet = gevent.spawn(requests.post, url, data=dumps(payload))
    greenlet.ready()
    greenlet.get()

    return

@post('/token/registerDeviceToken')
def registerDeviceToken() :
    requestBody = loads(request.body.read())
    token = requestBody['token']
    
    query = {'token' : token}
    tokenID = database.find(database="brazaar2",
                            collection="devices",
                            query=query)
    if not tokenID :
        tokenID = database.insert(database="brazaar2",
                                    collection="devices",
                                    data=requestBody)

    if tokenID :
        return dumps(requestBody)
    else :
        response.status = 300
        return {'error': 'register token error'}

    return 

@post('/product/getNearbyProducts')
def getNearbyProducts():
    requestBody = loads(request.body.read())
    token = requestBody['token']
    location = requestBody['location']

    # search in cache first
    nearestProducts = None
    # key = str(token + 'getNearbyProducts')
    # nearestProducts = cache.get_cache(key)
    if not nearestProducts :
        # search in database
        query = {'location': {'$nearSphere':{
                                            '$geometry': { 'type' : 'Point' ,
                                                           'coordinates' : [location['longitude'],location['latitude']]}}}}

        nearestProducts = database.find(database="brazaar2", 
                                        collection="products",
                                        limit=10)
        nearestProducts = dumps(nearestProducts)
        # add to cache
        # cache.set_cache(key, nearestProducts)

    if nearestProducts :
        return nearestProducts
    else :
        response.status = 300
        return {'error': 'request collection error'}

def uploadImages(folderName, images) :
    counter = 0
    for image in images :
        # decode base 64 data
        fileItem = StringIO(base64.b64decode(image))
        # Test if the file was uploaded
        if fileItem:
            filename = 'image' + str(counter) + '.jpg'
            key_name = folderName + '/' + filename
            database.upload_image(key_name=key_name, bucket="brazaar",
                                 data=fileItem)
            message = 'The file "' + filename + '" was uploaded successfully'
        else:
            message = 'No file was uploaded'

        print message
        # increment image counter
        counter += 1

@post('/product/addProduct')
def addProduct():
    requestBody = loads(request.body.read())
    token = requestBody['token']
    product = requestBody['product']
    name = product['name']
    images = product['images']
    product.setdefault('quantity', 1)
    # delete images key
    del product['images']

    # # send notification to followers
    # user = "Lunayo"
    # content = user + " has posted new product : " + name + "!"

    # #  simulate 10 followers
    # token = randomword(15)
    # for i in range(1,10) :
        # sendNotification(token=token, content=content)

    productID = database.insert(database="brazaar2", 
                                collection="products",
                                data=dict(product))

    if productID :
        greenlet = gevent.spawn(uploadImages, str(productID), images)
        greenlet.ready()
        greenlet.get()

        return dumps(product)
    else :
        response.status = 300
        return {'error': 'insert to collection error'}

@post('/product/getImages')
def getImages():
    requestBody = loads(request.body.read())
    token = requestBody['token']
    product = requestBody['product']
    productID = product['id']
    images = []

    if productID :
        images = database.get_images(key_name=productID, bucket="brazaar")

    # append images in to product json
    product['images'] = images

    return product

@post('/user/addFollowing')
def addFollowing():
    requestBody = loads(request.body.read())
    token = requestBody['token']
    relationship = requestBody['relationship']
    username = relationship['username']
    following = relationship['following']
    # check if user exists
    query = {"username" : username}
    user = database.find(database="brazaar2",
                         collection="users",
                         query=query)

    if user :
        followingID = database.insert(database="brazaar2",
                                        collection="followings",
                                        data=relationship)
        if followingID :
            return dumps(relationship)
        else :
            response.status = 300
            return {'error': 'Relationship exists'}
    else :
        response.status = 300
        return {'error': 'User not exists'}

@post('/user/getFollowers')
def getFollowers() :
    requestBody = loads(request.body.read())
    token = requestBody['token']
    username = requestBody['username']

    # check if user exists
    query = {"username" : username}
    user = database.find(database="brazaar2",
                         collection="users",
                         query=query)
    if user :
        #  get followers with username
        query = {'following' : username}
        followings = list(database.find(database="brazaar2",
                                        collection="followings",
                                        query=query))
        followingArray = []
        for following in followings:
            followingArray.append(following['username'])
        # append to request body
        requestBody['followings'] = followingArray
        return dumps(requestBody)
                
    else :
        response.status = 300
        return {'error': 'User not exists'}


# @post('/user/addFollower')
# def addFollower():
#     relationship = {}
#     session = {'username':"samatase"}
#     requestBody = loads(request.body.read())
#     token = requestBody['token']
#     relationship['following'] = requestBody['username']
#     relationship['user'] = session['username']

#     userQuery = '{"username":' + relationship['following'] + '}'
#     validate = list(database.find(database="brazaar2", 
#                                  collection="users",
#                                  query=userQuery))

#     if validate :
#         relationshipID = database.insert(database="brazaar2", 
#                                         collection="relationships",
#                                         data=dict(relationship))
#         return dumps(relationship)
#     else :
#         response.status = 300
#         return {'error': 'Invalid username'}

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

# @get ('/user/getFollowings')
# def getFollowing():
#     session = {'username':"samatase"}
#     followingUsers = []
#     requestBody = loads(request.body.read())
#     user = session['username']

#     followingsQuery = '{"user":user},{"following":1,"_id":0}'
#     followings = list(database.find(database="brazaar2", 
#                                     collection="relationships",
#                                     query=followingsQuery))

#     usersQuery = '{"username":' + following['following'] + '},{"firstName":1,"lastName":1,"_id":0}'
#     for following in followings:
#         user = database.find(database="brazaar2", 
#                             collection="users",
#                             query=usersQuery,
#                             limit=1)
#         if user :
#             followingUsers.append(list(user))
#         else :
#             return {'error' : 'invalid user'}

#     return dumps(followingUsers)

run(host='0.0.0.0', port=8080, debug=True, reloader=True, server="gevent")
# run(host='0.0.0.0', port=8082, debug=True)