import requests
import os
GEOCODE_XYZ_KEY = os.getenv("GEOCODE_XYZ_KEY")
def geocode_location(name):
    print(name)
    # try:
    #     url = f"https://nominatim.openstreetmap.org/search?q={name}&format=json"
    #     headers = {"User-Agent": "real-estate-chatbot"}
    #     res = requests.get(url, headers=headers)
    #     data = res.json()
    #     print(data)
    #     if data:
    #         return {
    #             "loc_name": data[0]["display_name"],
    #             "loc_lat": float(data[0]["lat"]),
    #             "loc_lon": float(data[0]["lon"])
    #         }
    # except Exception as e:
    #     print("Geocoding failed:", e)
    # return {}
    
    try:
        params = {
            "auth": GEOCODE_XYZ_KEY,
            "locate": name,
            "json": 1
        }
        geo_res = requests.get("https://geocode.xyz", params=params, timeout=10)
        geo_data = geo_res.json()
        if "latt" in geo_data and "longt" in geo_data:
            return {
                "loc_name": geo_data.get("standard", {}).get("addresst", name),
                "loc_lat": float(geo_data["latt"]),
                "loc_lon": float(geo_data["longt"])
            }
        else:
            print("geocode.xyz returned:", geo_data)
    except Exception as e:
        print("geocode.xyz failed:", e)

    return {}
