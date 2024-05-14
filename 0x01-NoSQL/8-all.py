#!/usr/bin/env python3
""" list all """
from pymongo import MongoClient


def list_all(mongo_collection):
    """ list all docs """
    return mongo_collection.find()
