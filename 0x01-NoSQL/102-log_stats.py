#!/usr/bin/env python3
""" get from nginx """
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    print(f"{collection.count_documents({})} logs")
    print("Methods:")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    for method in methods:
        count = collection.count_documents({'method': method})
        print(f"\tmethod {method}: {count}")

    stat = collection.count_documents({'method': 'GET', 'path': '/status'})
    print(f"{stat} status check")

    print("IPs:")
    pipeline = [
            {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
            ]

    top_ips = collection.aggregate(pipeline)

    for index, ip_data in enumerate(top_ips, 1):
        ip = ip_data['_id']
        count = ip_data['count']
        print(f"\t{ip}: {count}")
