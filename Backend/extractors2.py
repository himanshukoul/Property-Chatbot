import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EXTRACTION_PROMPT_COMMON = """
You are a real estate assistant.Extract structured data from the user's message
Fields already provided by the user so far (if any):
{prev_msg}
User Message:
"{user_msg}"

Respond only in this JSON format:
{{
  "data":{{
  "intent": "search" | "post" ,
  "listing_type": "sale or rent",
  "property_type": "apartment, villa, plot, commercial, etc.",
  "location": {{
      "city": "city name",
      "locality": "local area or neighborhood"
    }},
  "bedrooms": number 
  }},
  "user_message": "rich message that summarizes what has been captured which later be used for semantic search",
  "bot_reply": "friendly message that clearly lists any missing fields"
}}
Instructions:
+ Return only the JSON, and do NOT wrap it in backticks or markdown.
+ DO NOT end JSON with a comma.
1. Extract all filters that are clearly mentioned.
2. For missing or ambiguous filters,omit from `data`,and write polite and clear questions to ask about missing details.
3. Keep the `data` key clean and structured for backend usage.
4. We can update the fields even if it's previously given by user.
"""

EXTRACTION_PROMPT_SEARCH = """
You are a helpful assistant for a real estate chatbot. A user is trying to search for a property to buy or rent. Your job is to extract all relevant search filters and return them as a structured JSON object along with a user-friendly response.

Fields already provided by the user so far (if any):
{prev_msg}
User Message:
"{user_msg}"

Your output must follow this format:
{{
  "data": {{
    "intent": "search" | "post",
    "listing_type": "sale or rent",
    "property_type": "apartment, villa, plot, commercial, etc.",
    "price_min": numeric value (in INR),
    "price_max": numeric value (in INR),
    "area_min": numeric area (in sqft),
    "area_max": numeric area (in sqft),
    "bedrooms": number (if applicable),
    "bathrooms": number (if applicable),
    "furnishing": "furnished, semi-furnished, unfurnished (if applicable)",
    "available_from": "date(yyyy-mm-dd) or 'immediately'",
    "location": {{
      "city": "city name",
      "locality": "local area or neighborhood"
    }},
    "preferred_floor_min": "ground or number",
    "preferred_floor_max": "ground or number",
    "ownership": "freehold, leasehold, etc.",
    "property_age_min": number (in years),
    "property_age_max": number (in years)
  }},
  "user_message": "rich message that summarizes what has been captured which later be used for semantic search",
  "bot_reply": "friendly message that clearly lists any missing fields"
}}

Instructions:
+ Return only the JSON, and do NOT wrap it in backticks or markdown.
+ DO NOT end JSON with a comma.
1. Extract all filters that are clearly mentioned.
2. For missing or ambiguous filters,omit from `data`, and write polite and clear questions to ask about missing details.
3. Keep the `data` key clean and structured for backend usage.
4. Change intent to post only when you are fully sure.
5. Convert values wherever required.
6. We can update the fields even if it's previously given by user.
7. If everything is provided, respond with a confirmation like: “Thanks! Here's what I’ll search for...”
"""

EXTRACTION_PROMPT_POST = """
You are a helpful assistant for a real estate chatbot. A user is trying to post their property for sale or rent. Your job is to collect **all required property information** and return it as a **structured JSON object** along with a **user-friendly message**.
Fields already provided by the user so far (if any):
{prev_msg}
User Message:
"{user_msg}"
Your output must follow this format:
{{
  "data": {{
    "intent": "search" | "post",
    "listing_type": "sale or rent",
    "property_type": "apartment, villa, plot, commercial, etc.",
    "price": "numeric value (in INR)",
    "area": "numeric area (in sqft)",
    "bedrooms": "number (if applicable)",
    "bathrooms": "number (if applicable)",
    "furnishing": "furnished, semi-furnished, unfurnished (if applicable)",
    "available_from": "date(yyyy-mm-dd) or 'immediately'",
    "location": {{
      "city": "city name",
      "locality": "local area or neighborhood",
    }},
    "amenities": e.g. ["gym", "parking","clubhouse", ...],
    "floor_number": "number or 'ground'",
    "total_floors": "total number of floors in building",
    "ownership": "freehold, leasehold, etc.",
    "property_age": number (in years),
    "confirm": "boolean (True/False)"
  }},
  "user_message": "rich message that summarizes what has been captured which later be used for semantic search",
  "bot_reply": "friendly message that clearly lists any missing fields",
}}

Instructions:
+ Return only the JSON, and do NOT wrap it in backticks or markdown.
+ DO NOT end JSON with a comma.
1. Extract all the information provided by the user.
2. For missing or ambiguous filters,omit from `data`, and write polite and clear questions to ask about missing details.
3. Change intent to search only when you are fully sure.
4. Convert values wherever required.
5. Once all data fields are provided, ask for confirmation before proceeding.
6. Add confirm as True only if every field is filled and user explicitly confirms. Otherwise set confirm: false.
7. If everything is provided and confirmed, respond with a confirmation like: “Your property has been successfully posted! and ask for photos to make it more attractive”.
"""


def extract_fields_from_query(user_msg,prev_fields,mode):
    prev_msg = json.dumps(prev_fields)
    print(prev_msg)
    if mode == "common":
        prompt = EXTRACTION_PROMPT_COMMON.format(user_msg=user_msg,prev_msg=prev_msg)
    elif mode == "search":
        prompt = EXTRACTION_PROMPT_SEARCH.format(user_msg=user_msg,prev_msg=prev_msg)
    else:
        prompt = EXTRACTION_PROMPT_POST.format(user_msg=user_msg,prev_msg=prev_msg)
        
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    content = response.choices[0].message.content
    print("content is: ", content)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("Invalid JSON from OpenAI:", content)
        try:
          fixed = content.strip().rstrip(",}") + "}"
          return json.loads(fixed)
        except Exception:
          return {}
    # I want a house in Mayur Vihar. It should be around 50 lakhs. Should have good schools and malls nearby.
    # i want a house having hospitals and schools for children nearby, i also want park in that region
    # content = {
    #   "intent": "search",
    #   "search_type": "buy",
    #   "location": {
    #       "city": "Delhi",
    #       "locality": "Mayur Vihar",
    #     },
    #   "price_min": 4500000,
    #   "price_max": 5500000
    # }
    # postcontent = {
    #   "intent": "post",
    #   "post_type": "rent_out",
    #   "location": "Mayur Vihar",
    #   "price": 5000000,
    #   "bhk": 3,
    #   "property_type": "Apartment",
    #   "furnishing": "Semi-furnished",
    #   "area": 1000,
      
    # }
    
    # return content