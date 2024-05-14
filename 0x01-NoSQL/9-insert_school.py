#!/usr/bin/env python3
""" 9-main """
from pymongo import MongoClient

def insert_school(mongo_collection, **kwargs):
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
