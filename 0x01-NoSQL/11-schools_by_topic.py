#!/usr/bin/env python3
""" 11-main """
from pymongo import MongoClient


def schools_by_topic(mongo_collection, topic):
    """ search by topic """
    return mongo_collection.find({"topics": topic})
