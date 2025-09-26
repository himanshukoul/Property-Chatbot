import os
from pymongo.server_api import ServerApi
from pymongo import MongoClient, GEOSPHERE
import load_env

uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi("1"))

db = client.real_estate
db_listings = db.listings
db_listings.create_index([("location_point", GEOSPHERE)])
db_users = db.users
db_users.create_index("email", unique=True)
def post_listings(doc):
    db_listings.insert_one(doc)

def query_mongodb(filters, ids=None, lat=None, lon=None, limit=10):
    query = filters.copy()

    if ids:
        query["_id"] = {"$in": ids}

    if lat is not None and lon is not None:
        query["location_point"] = {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "$maxDistance": 5000  # 5km search radius
            }
        }

    return list(db_listings.find(query).limit(limit))
