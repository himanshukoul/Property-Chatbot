import requests
import os

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY") 

def geocode_location(name):
    print("Geocoding:", name)
    try:
        params = {
            "address": name,
            "key": GOOGLE_MAPS_API_KEY
        }
        response = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=params, timeout=10)
        data = response.json()

        if data["status"] == "OK" and data["results"]:
            top_result = data["results"][0]
            geometry = top_result["geometry"]["location"]

            return {
                "loc_name": top_result["formatted_address"],
                "loc_lat": float(geometry["lat"]),
                "loc_lon": float(geometry["lng"])
            }

        print("Google Maps returned:", data.get("status"), data.get("error_message"))
    except Exception as e:
        print("Google Maps Geocoding failed:", e)

    return {}
