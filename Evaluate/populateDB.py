from pymongo import GEO2D

__author__ = 'Emmanouil Samatas'

import pymongo
connectionString = "mongodb://localhost"
connection = pymongo.MongoClient(connectionString)
db = connection.brazaar
products = db.products

def populateDb():
#id name description location:[lat, long] price quantity user_id
    sampleName = 'iPhone 5'
    sampleDescription = 'Latest Apple smart phone'
    samplePrice = {'value':10000,'currency' :"GBP"}
    user_id = 0
    sampleQuantity = 1
    sampleLocation = {'long' : -10.20 , 'lat' : 20.20}

    for i in range(0,50):
        sampleLocation['lat'] += 0.10
        sampleLocation['long'] += 0.10
        products.insert({'name':sampleName,
                         'description':sampleDescription,
                         'price' : samplePrice ,
                         'user' : user_id ,
                         'quantity' : sampleQuantity ,
                         'location' : sampleLocation})

def indexDb():
    products.create_index([('location',GEO2D)])

populateDb()
indexDb()

print products.find_one()

