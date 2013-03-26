__author__ = 'Emmanouil Samatas'

import pymongo
import math
connectionString = "ec2-54-228-150-22.eu-west-1.compute.amazonaws.com:27017"
connection = pymongo.MongoClient(connectionString)
db = connection.brazaar
products = db.products

def calculateDistance(longFrom ,latFrom  , longTo , latTo):
    return math.sqrt(((longTo - longFrom) ** 2) + ((latTo - latFrom)** 2))

