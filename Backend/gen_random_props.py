import load_env
import time
import uuid
import random
from pymongo import MongoClient
from config import DevelopmentConfig
from geocode import geocode_location
from pinecone_client import upsert_listing

cities_with_localities = {
    "Delhi": ["Mayur Vihar", "Uttari Pitampura", "Lajpat Nagar"],
    "Noida": ["Sector 150", "Sector 76", "Sector 137"],
    "Bangalore": ["Whitefield", "HSR Layout", "Koramangala"],
    "Chennai": ["T. Nagar", "Velachery", "Adyar"]
}

property_types = ["apartment", "villa", "plot", "commercial"]
furnishing_options = ["furnished", "semi-furnished", "unfurnished"]
ownerships = ["freehold", "leasehold"]
available_from_options = ["immediately", "2027-03-01", "2026-02-15", "2025-11-20"]
amenities_pool = ["gym", "pool", "clubhouse", "parking", "lift", "park", "security", "kids area"]
listing_types = ["sale", "rent"]

client = MongoClient(DevelopmentConfig.MONGO_URI)
db = client.real_estate
listings = db.listings


def get_coordinates(full_location):
    try:
        geo = geocode_location(full_location)
        if geo:
            return  geo["loc_name"],float(geo["loc_lon"]), float(geo["loc_lat"])
    except Exception as e:
        print("Geocode error:", e)
    return None


def generate_description(city, locality, bhk, prop_type, furnish, price, area, amenities, floor_number, total_floors, ownership, property_age, available_from, listing_type):
    main_info = [
        f"{bhk} BHK {furnish} {prop_type} available for {listing_type} in {locality}, {city}.",
        f"Spanning {area} sqft, it's located on floor {floor_number} of a {total_floors}-floor building.",
        f"Ownership is {ownership}, and the property is around {property_age} old.",
        f"Available from {available_from}.",
        f"Key amenities include {', '.join(amenities)}."
    ]

    natural_phrases = [
        "Ideal for families looking for a peaceful neighborhood.",
        "Located close to daily conveniences and transport.",
        "Well-ventilated and gets good sunlight.",
        "In a gated society with 24/7 security.",
        "Walking distance to markets and cafes."
    ]

    selected_phrases = random.sample(natural_phrases, random.randint(1, 3))
    return " ".join(main_info + selected_phrases)


def generate_listing():
    city = random.choice(list(cities_with_localities.keys()))
    locality = random.choice(cities_with_localities[city])
    bhk = random.randint(1, 4)
    prop_type = random.choice(property_types)
    furnish = random.choice(furnishing_options)
    listing_type = random.choice(listing_types)
    price = random.randint(30, 90) * 100000 if listing_type == "sale" else random.randint(10, 50) * 10000
    area = random.randint(800, 1800)
    available_from = random.choice(available_from_options)
    ownership = random.choice(ownerships)
    bathrooms = random.randint(1, bhk)
    amenities = random.sample(amenities_pool, random.randint(2, 5))
    floor_number = random.randint(0, 5)
    total_floors = floor_number + random.randint(1, 10)
    property_age = f"{random.randint(1, 10)} years"

    time.sleep(1)  
    coords = get_coordinates(f"{locality}, {city}")
    if coords is None:
        return None
    loc_name, lon, lat = coords

    doc_id = str(uuid.uuid4())
    desc = generate_description(
        city, locality, bhk, prop_type, furnish, price, area,
        amenities, floor_number, total_floors, ownership,
        property_age, available_from, listing_type
    )

    doc = {
        "_id": doc_id,
        "user_id": "dummy",
        "user_name": "dummy",
        "city": city,
        "location": loc_name,
        "listing_type": listing_type,
        "property_type": prop_type,
        "ownership": ownership,
        "price": price,
        "area": area,
        "bedrooms": bhk,
        "bathrooms": bathrooms,
        "furnishing": furnish,
        "available_from": available_from,
        "amenities": amenities,
        "floor_number": floor_number,
        "total_floors": total_floors,
        "property_age": property_age,
        "description": desc,
        "location_point": {
            "type": "Point",
            "coordinates": [lon, lat]
        },
        "images":[]
    }

    return doc


def insert_listings(n):
    inserted = 0
    for _ in range(n * 2):  
        if inserted >= n:
            break
        listing = generate_listing()
        if listing:
            listings.insert_one(listing)
            upsert_listing(listing["_id"], listing["description"])
            print(f"Inserted: {listing['_id']} | {listing['listing_type']} | {listing['city']}, {listing['location']} | ₹{listing['price']}")
            inserted += 1
        else:
            print(" Skipped (Geocode failed)")


if __name__ == "__main__":
    insert_listings(30)
