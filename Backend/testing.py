from mem0_client import upsert_memory
upsert_memory(
                user_id=123,
                description=" User want a house in Mayur Vihar. It should be around 50 lakhs. Should have good schools and malls nearby",
                intent="search",
                metadata= {
 "intent":"search",
 "loc_lat":28.6182925,
 "loc_lon":77.30731329999999,
 "loc_name":"Pocket-C, Mayur Vihar Phase II, Mayur Vihar, Delhi, 110091, India",
 "location":{
   "city":"Mayur Vihar",
   "locality":"Pocket C"
  },
 "price_max":5500000,
 "price_min":4500000,
 "description":" User want a house in Mayur Vihar. It should be around 50 lakhs. Should have good schools and malls nearby",
 "listing_type":"sale or rent",
 "property_type":"apartment, villa, plot, commercial, etc."
}
            )
