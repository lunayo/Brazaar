from pymongo import GEO2D, GEOSPHERE
from random import uniform

__author__ = 'Emmanouil Samatas'

import pymongo
connectionString = "ec2-54-228-150-22.eu-west-1.compute.amazonaws.com:27017"
connection = pymongo.MongoClient(connectionString)
db = connection.brazaar
products = db.products

def assignRandomLocation():
    long = round(uniform(-180 , 180),6)
    lat = round(uniform(-90 , 90),6)
    return {'longitude':  long , 'latitude' : lat }

def populateDb():
#id name description location:[lat, long] price quantity user_id
    sampleName = 'sampleProduct'
    sampleDescription = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum'
    samplePrice = {'value':10000,'currency' :"GBP"}
    user_id = 0
    sampleQuantity = 1

    products.drop()

    for i in range(0,10**3):
       products.insert({'name':sampleName,
                         'description':sampleDescription,
                         'price' : samplePrice ,
                         'user' : user_id ,
                         'quantity' : sampleQuantity ,
                         'location' : assignRandomLocation()})

def indexDb():
    products.create_index([('location',GEOSPHERE)])

populateDb()
#indexDb()

print products.find_one()

