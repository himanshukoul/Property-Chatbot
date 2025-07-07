**Property Chatbot Frontend**
**Overview**
This is the frontend for a real estate chatbot application built with React, Vite, and Material-UI. It provides a user-friendly interface for searching and posting properties, interacting with a chatbot, and managing user authentication. The frontend communicates with a Flask-based backend via SocketIO for real-time chat and REST APIs for authentication and memory retrieval.

**Features**

User Authentication: Login and signup dialogs for user authentication with JWT tokens.
Property Search: Search bar to initiate property searches with natural language queries.
Real-time Chat: Interactive chatbot for property searches and postings using SocketIO.
Property Display: Card-based display of property listings with hover effects.
Session Management: Resume previous sessions using saved memories from the backend.
Responsive Design: Styled with Material-UI and custom CSS for a modern, responsive UI.

**Prerequisites**

Node.js 16+
Backend server running at http://localhost:5000 (see backend README for setup)
Internet access for CDN-hosted dependencies (Font Awesome, SocketIO client)

Setup Instructions

cd Frontend

1.  Install Dependencies
    npm install
    This installs all required dependencies listed in package.json, including:

            react
            react-dom
            @mui/material
            @mui/icons-material
            jwt-decode
            socket.io-client
            uuid

2.  Ensure Backend is Running

The frontend expects the backend server to be running at http://localhost:5000.
Follow the backend setup instructions to start the Flask server with SocketIO.

3. Run the Application
   npm run dev

This starts the Vite development server,at http://localhost:5173. Open this URL in your browser to access the application.

Open http://localhost:5173 in your browser.
The landing page displays a navbar, search bar, and property cards (if any).

**User Authentication**

Signup: Click "Signup" in the navbar to register with an email and password.
Login: Click "Login" to authenticate with existing credentials.
Upon successful login/signup, a JWT token is stored in localStorage, and the user’s email is displayed in the navbar.

**Property Search**

Use the search bar to enter queries like: Find a 2 BHK apartment in Delhi under 50 lakhs.
The query is sent to the backend via SocketIO, and matching properties are displayed as cards.
Properties include details like location, price, and description.

**Chatbot Interaction**

After initiating a search, the chatbot window appears.
Interact with the bot by typing messages (e.g., I want to post a villa in Noida).
The bot guides you through providing required fields (e.g., price, area) and confirms postings.
Chat history is displayed.

**Resume Previous Sessions**

On login, a dialog shows recent session memories (if any).
Select a memory to resume a previous search/posting or choose "Start Fresh" for a new session.

**Logout**

Click "Logout" in the navbar to clear the JWT token and reset the session.

Dependencies

React: Frontend library for building the UI.
Material-UI: For styled components and dialogs.
SocketIO Client: For real-time communication with the backend.
jwt-decode: For decoding JWT tokens to check validity.
uuid: For generating unique IDs for chat messages.
Font Awesome: For icons in the navbar and memory dialog.

Notes

Ensure the backend is running before starting the frontend to avoid connection errors.
The frontend uses localStorage to persist JWT tokens and user email.
Property images default to /assets/no-image.jpg if not provided by the backend.
The application is responsive but optimized for desktop.
