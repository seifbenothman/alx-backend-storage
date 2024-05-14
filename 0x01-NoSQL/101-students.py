#!/usr/bin/env python3
""" Aggregate """
from pymongo import MongoClient


def top_students(mongo_collection):
    """retunr sorted average score"""
    return mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
                }
            },
        {"$sort": {"averageScore": -1}}
        ])
