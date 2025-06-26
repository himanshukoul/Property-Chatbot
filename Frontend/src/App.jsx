import "./App.css";
import { useState, useEffect } from "react";
import Navbar from "./Components/Navbar.jsx";
import SearchBar from "./Components/SearchBar.jsx";
import ChatBot from "./Components/ChatBot.jsx";
import DisplayCards from "./Components/DisplayCards.jsx";
import LoginDialog from "./Components/LoginDialog.jsx";
import SignupDialog from "./Components/SignupDialog.jsx";
import { jwtDecode } from "jwt-decode";
import socket from "./static/socket.js";
import { v4 as uuidv4 } from "uuid";

import { createTheme, ThemeProvider } from "@mui/material/styles";
const theme = createTheme({
  palette: {
    primary: {
      main: "#157c63",
    },
    secondary: {
      main: "#FF7300",
    },
  },
});

function App() {
  const [chatStarted, setChatStarted] = useState(false);
  const [properties, setProperties] = useState([]);
  const [chatHistory, setChatHistory] = useState([]);
  const [waitingResponse, setWaitingResponse] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null);
  const [showLogin, setShowLogin] = useState(false);
  const [showSignup, setShowSignup] = useState(false);

  const checkTokenValidity = () => {
    const token = localStorage.getItem("token");
    if (!token) return false;
    try {
      const decoded = jwtDecode(token);
      const currentTime = Date.now() / 1000;
      if (!decoded.exp || decoded.exp < currentTime) {
        localStorage.removeItem("token");
        localStorage.removeItem("email");
        setIsLoggedIn(false);
        setUserData(null);
        setShowLogin(true);
        setChatHistory((prev) => [
          ...prev,
          {
            id: uuidv4(),
            sender: "bot",
            message: "Session expired. Please log in.",
          },
        ]);
        return false;
      }
      return true;
    } catch (err) {
      localStorage.removeItem("token");
      localStorage.removeItem("email");
      setIsLoggedIn(false);
      setUserData(null);
      setShowLogin(true);
      setChatHistory((prev) => [
        ...prev,
        {
          id: uuidv4(),
          sender: "bot",
          message: "Invalid token. Please log in.",
        },
      ]);
      return false;
    }
  };
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token && checkTokenValidity()) {
      setIsLoggedIn(true);
      const email = localStorage.getItem("email");
      setUserData({ email });
    }
    socket.on("bot_response", (data) => {
      setWaitingResponse(false);
      if (
        data.message === "Authentication required" ||
        data.message === "Invalid or expired token"
      ) {
        localStorage.removeItem("token");
        localStorage.removeItem("email");
        setIsLoggedIn(false);
        setUserData(null);
        setShowLogin(true);
        setChatHistory((prev) => [
          ...prev,
          {
            id: uuidv4(),
            sender: "bot",
            message: "Please log in to continue.",
          },
        ]);
      } else if (data.message) {
        setChatHistory((prev) => [
          ...prev,
          { id: uuidv4(), sender: "bot", message: data.message },
        ]);
      }
      if (data.properties) {
        setProperties(data.properties);
      }
    });
    return () => {
      socket.off("bot_response");
    };
  }, [setChatHistory, setProperties]);

  const handleInitialSearch = (query) => {
    console.log("Init search");
    if (!checkTokenValidity()) {
      setShowLogin(true);
      setChatHistory((prev) => [
        ...prev,
        { id: uuidv4(), sender: "bot", message: "Please log in to search." },
      ]);
      return;
    }
    const token = localStorage.getItem("token");
    socket.auth = { token };
    socket.emit("message", { msg: query, token });
    console.log("emitted msg", query);
    setWaitingResponse(true);
    setChatHistory((prev) => [
      ...prev,
      { id: uuidv4(), sender: "user", message: query },
    ]);
    setChatStarted(true);
  };
  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("email");
    setIsLoggedIn(false);
    setUserData(null);
    setChatHistory([]);
    setProperties([]);
    setChatStarted(false);
  };
  return (
    <ThemeProvider theme={theme}>
      <Navbar
        isLoggedIn={isLoggedIn}
        userData={userData}
        setShowLogin={setShowLogin}
        setShowSignup={setShowSignup}
        handleLogout={handleLogout}
      />
      <SearchBar handleInitialSearch={handleInitialSearch} />

      <div className="main-content">
        <div
          className={chatStarted ? "card-section half" : "card-section full"}
        >
          <DisplayCards theme={theme} properties={properties} />
        </div>

        {chatStarted && (
          <div className="chat-section">
            <ChatBot
              chatHistory={chatHistory}
              setChatHistory={setChatHistory}
              setProperties={setProperties}
              setWaitingResponse={setWaitingResponse}
              waitingResponse={waitingResponse}
              checkTokenValidity={checkTokenValidity}
            />
          </div>
        )}
        <LoginDialog
          open={showLogin}
          onClose={() => setShowLogin(false)}
          setIsLoggedIn={setIsLoggedIn}
          setUserData={setUserData}
        />
        <SignupDialog
          open={showSignup}
          onClose={() => setShowSignup(false)}
          setIsLoggedIn={setIsLoggedIn}
          setUserData={setUserData}
        />
      </div>
    </ThemeProvider>
  );
}

export default App;
