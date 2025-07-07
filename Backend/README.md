**Property Chatbot Backend
Overview**
This is the backend for a real estate chatbot application built with Flask and SocketIO. It supports user authentication, property search, property posting,and user preference functionalities. The application uses MongoDB for data storage, Pinecone for vector search, OpenAI for natural language processing, Mem0.ai for storing user preferences and Google Maps for geocoding. It also includes email notifications for property matches.

**Features**
•	User Authentication: Signup and login with JWT based authentication.
•	Real-time Interaction: SocketIO for real-time chat and property updates.
•	Property Search: Semantic search using Pinecone and MongoDB with geospatial queries.
•	Property Posting: Users can post properties with detailed fields and receive confirmation.
•	Email Notifications: Alerts users when new properties match their preferences.
•	Session Management: Handles user sessions with automatic memory upsertion for idle sessions.
•	User Preferences: Handles user past history for smooth conversation.

**Prerequisites**
•	Python 3.8+
•	MongoDB (local or cloud instance)
•	API keys for:
- OpenAI (OPENAI_API_KEY)
- Pinecone (PINECONE_API_KEY)
- Google Maps (GOOGLE_MAPS_API_KEY)
- Mem0 (MEM0_API_KEY)
- Email service (EMAIL_ADDRESS, APP_PASSWORD)

**Setup Instructions**
cd Backend

1. Create a Virtual Environment
python -m venv venv
venv\Scripts\activate
2. Install Dependencies
pip install -r requirements.txt
3. Configure Environment Variables
Create a .env file in the project root and add the following:
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
MEM0_API_KEY=your_mem0_api_key
EMAIL_ADDRESS=your_email_address
EMAIL_PASSWORD=your_app_password
5. Set Up MongoDB
•	Ensure MongoDB is running locally on mongodb://localhost:27017/ or update the MONGO_URI in config.py if using a cloud instance.
•	The database real_estate will be created automatically with collections listings and users.
•	While initially creating listing db , uncomment the following once:
#db_listings.create_index([("location_point", GEOSPHERE)])
6. Initialize Pinecone
•	Ensure the Pinecone index description-dense-py is created automatically on startup (configured in pinecone_config.py).
•	Verify your Pinecone API key and region (us-east-1 by default).
7. Run the Application
python app2.py
The server will start on http://localhost:5000 with SocketIO enabled.
Usage

**API Endpoints**
-	GET /: Health check endpoint to verify the backend is running.
-	POST /api/signup: Register a new user.
    -	Payload: { "email": "user@example.com", "password": "password" }
    -	Response: { "token": "jwt_token", "email": "user@example.com" }
-	POST /api/login: Authenticate a user.
    -	Payload: { "email": "user@example.com", "password": "password" }
    -	Response: { "token": "jwt_token", "email": "user@example.com" }
-	GET /api/memories: Fetch recent user memories (requires Bearer token).
    -	Header: Authorization: Bearer <jwt_token>
    -	Response: { "memories": [...] }

**SocketIO Events**
-	connect: Authenticate with { "token": "jwt_token" } in auth parameter.
-	message: Send user messages to interact with the chatbot.
-	Payload: { "msg": "I want a house in Mayur Vihar for 50 lakhs" }
-	Response: { "message": "bot response", "properties": [...] }

**Example Interaction**
**Property Post**
1.	Connect to SocketIO with a valid JWT token.
2.	Send a message like: I want to post a 3 BHK apartment in Mayur Vihar for rent.
3.	The bot responds with prompts for missing fields (e.g., price, area).
4.	Provide details until all required fields are filled.
5.	Confirm the posting with confirm or post it.
6. Confirm to post the listing, which is saved to MongoDB and  Pinecone.
7. 	Matching users receive email alerts.
8.	Receive a confirmation and a prompt to upload photos.

**Property Search**
1.	Send a search query like: Find a 2 BHK apartment in Delhi under 50 lakhs.
2.	The bot extracts filters, performs a hybrid search (Pinecone + MongoDB), and returns matching properties.


##### Once enough fields are taken (3 here) , user responses are saved in Mem0.ai , either after 10 mins of inactivity on chat, or once backend shuts down.

**Notes**
•	Ensure all API keys are valid and have sufficient quotas.
•	MongoDB indexes are created automatically for users.email (unique) and listings.location_point (geospatial).
•	The application uses a background thread to save idle sessions to Mem0 every 10 minutes.
•	On shutdown, all active sessions are saved to Mem0.
•	The frontend (in Frontend Readme) should connect to SocketIO at ws://localhost:5000 and handle JWT tokens.


