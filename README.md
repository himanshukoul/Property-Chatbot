# Real Estate Chatbot (Proppy)


This is a full stack real estate chatbot application built with a Flask backend and a React frontend using Vite and Material-UI. 
It supports user authentication, property search, property posting, viewing user listings, image uploads for listings, and real time chat interactions. 
The backend uses MongoDB for data storage, Pinecone for vector search, OpenAI for natural language processing, Mem0.ai for storing user preferences, and Google Maps for geocoding.
Email notifications are sent for property matches, and SocketIO enables real time communication.


## Features


<b> User Authentication: </b> Signup and login with JWT based authentication.



<b>Real time Interaction:</b> SocketIO for real time chat and property updates.



<b>Property Search:</b> Semantic search using Pinecone and MongoDB with geospatial queries.



<b>Property Posting:</b> Users can post properties with detailed fields and receive confirmation.



<b>View My Listings:</b> Users can view, and delete their posted listings.



<b>Image Uploads:</b> Users can upload images for their property listings.



<b>Email Notifications:</b> Alerts users when new properties match their preferences.



<b>Session Management:</b> Handles user sessions with automatic memory upsertion for idle sessions.



<b>User Preferences:</b> Stores user interaction history for smooth conversation resumption.



<b>Responsive Design:</b> Modern, responsive UI with Material-UI and custom CSS.



## Setup Instructions


### Backend


cd Backend


Create a Virtual Environment:


 &nbsp; &nbsp;&nbsp; &nbsp; python -m venv venv


&nbsp; &nbsp;&nbsp; &nbsp; venv/Scripts/activate


pip install -r requirements.txt


Enable 2-Step Verification on your Google account and then create app password here : https://myaccount.google.com/apppasswords


Configure Environment Variables:


&nbsp; &nbsp;&nbsp; &nbsp; OPENAI_API_KEY=""


&nbsp; &nbsp;&nbsp; &nbsp; PINECONE_API_KEY=""


&nbsp; &nbsp;&nbsp; &nbsp; GOOGLE_MAPS_API_KEY=""


&nbsp; &nbsp;&nbsp; &nbsp; MEM0_API_KEY=""


&nbsp; &nbsp;&nbsp; &nbsp; EMAIL_ADDRESS="email address"


&nbsp; &nbsp;&nbsp; &nbsp; EMAIL_PASSWORD="app password ( not normal gmail password)"


### Set Up MongoDB


Ensure MongoDB is running locally on mongodb://localhost:27017/ or update MONGO_URI in config.py for a cloud instance.


The database real_estate will be created automatically with collections listings and users.


### Initialize Pinecone


python pinecone_config.py 


Ensure the Pinecone index description-dense-py is created.


### Run the Backend


python app2.py


## Frontend Setup


cd Frontend


npm install


Ensure Backend is Running. The frontend expects the backend at http://localhost:5000. Follow backend setup first.


npm run dev


## Usage


### API Endpoints (Backend)


<b> GET /: Health check to verify the backend is running. </b>


Response: "Backend running"


<b> POST /api/signup: Register a new user. </b>


Payload: { "email": "user@example.com", "password": "password" }


Response: { "token": "jwt_token", "email": "user@example.com" }


<b>POST /api/login: Authenticate a user.</b>


Payload: { "email": "user@example.com", "password": "password" }


Response: { "token": "jwt_token", "email": "user@example.com" }


<b>GET /api/memories: Fetch recent user memories (requires Bearer token).</b>


Header: Authorization: Bearer <jwt_token>


Response: { "memories": [...] }


<b>POST /api/upload_images/<listing_id>: Upload images for a listing.</b>


Payload: FormData with images field (multiple files).


Response: { "message": "Images uploaded", "urls": [...] }


<b> DELETE /api/delete_listing/<listing_id>: Delete a user’s listing. </b> 


Header: Authorization: Bearer <jwt_token>


Response: { "message": "Deleted" }


<b>GET /api/my_listings: Fetch user’s posted listings.</b>


Header: Authorization: Bearer <jwt_token>


Response: { "listings": [...] }


### SocketIO Events (Backend)


connect: Authenticate with { "token": "jwt_token" } in auth parameter.


message: Send user messages to interact with the chatbot.


Payload: { "msg": "I want a house in Mayur Vihar for 50 lakhs" }


Response: { "message": "bot response", "properties": [...] }



