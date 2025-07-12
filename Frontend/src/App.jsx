import "./App.css";
import { useState, useEffect } from "react";
import Navbar from "./Components/Navbar.jsx";
import SearchBar from "./Components/SearchBar.jsx";
import DisplayCards from "./Components/DisplayCards.jsx";
import LoginDialog from "./Components/LoginDialog.jsx";
import SignupDialog from "./Components/SignupDialog.jsx";
import ResumeMemoryDialog from "./Components/ResumeMemoryDialog.jsx";
import ChatDrawer from "./Components/ChatDrawer.jsx";

import { jwtDecode } from "jwt-decode";
import socket from "./static/socket.js";
import { v4 as uuidv4 } from "uuid";

import { createTheme, ThemeProvider } from "@mui/material/styles";
import { Fab } from "@mui/material";
import SmartToyIcon from "@mui/icons-material/SmartToy";

const theme = createTheme({
  palette: {
    primary: { main: "#157c63" },
    secondary: { main: "#FF7300" },
  },
});

function App() {
  const [chatDrawerOpen, setChatDrawerOpen] = useState(false);
  const [properties, setProperties] = useState([]);
  const [chatHistory, setChatHistory] = useState([]);
  const [waitingResponse, setWaitingResponse] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null);
  const [showLogin, setShowLogin] = useState(false);
  const [showSignup, setShowSignup] = useState(false);
  const [savedMemories, setSavedMemories] = useState([]);
  const [showMemoryDialog, setShowMemoryDialog] = useState(false);

  const checkTokenValidity = () => {
    const token = localStorage.getItem("token");
    if (!token) return false;
    try {
      const decoded = jwtDecode(token);
      const currentTime = Date.now() / 1000;
      if (!decoded.exp || decoded.exp < currentTime || !decoded.user_id) {
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
    } catch {
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

  const fetchMemories = () => {
    const token = localStorage.getItem("token");
    if (!token || !checkTokenValidity()) return;

    fetch("http://localhost:5000/api/memories", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data.memories)) {
          setSavedMemories(data.memories);
          setShowMemoryDialog(true);
        }
      })
      .catch(() => {
        setChatHistory((prev) => [
          ...prev,
          {
            id: uuidv4(),
            sender: "bot",
            message: "Failed to load past sessions. Please try again.",
          },
        ]);
        setShowMemoryDialog(false);
      });
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token && checkTokenValidity()) {
      setIsLoggedIn(true);
      setUserData({ email: localStorage.getItem("email") });
      socket.auth = { token };
      if (!socket.connected) socket.connect();
      fetchMemories();
    }
    return () => socket.disconnect();
  }, []);

  useEffect(() => {
    socket.on("connect", () => console.log("Socket connected"));

    socket.on("connect_error", (error) => {
      console.error("Socket connection error:", error.message);
      setChatHistory((prev) => [
        ...prev,
        {
          id: uuidv4(),
          sender: "bot",
          message: "Failed to connect to server.",
        },
      ]);
      setWaitingResponse(false);
    });

    socket.on("bot_response", (data) => {
      setWaitingResponse(false);
      if (
        ["Authentication required", "Invalid or expired token"].includes(
          data.message
        )
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
        return;
      }

      if (data.message) {
        setChatHistory((prev) => [
          ...prev,
          { id: uuidv4(), sender: "bot", message: data.message },
        ]);
      }

      if (data.properties) {
        setProperties(data.properties);
      }
    });

    socket.on("memory_popped", () => {
      if (checkTokenValidity()) fetchMemories();
    });

    return () => {
      socket.off("connect");
      socket.off("connect_error");
      socket.off("bot_response");
      socket.off("memory_popped");
    };
  }, [fetchMemories]);

  const handleInitialSearch = (query) => {
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
    if (!socket.connected) socket.connect();

    socket.emit("message", { msg: query });
    setWaitingResponse(true);
    setChatHistory((prev) => [
      ...prev,
      { id: uuidv4(), sender: "user", message: query },
    ]);
    setChatDrawerOpen(true);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("email");
    setIsLoggedIn(false);
    setUserData(null);
    setChatHistory([]);
    setProperties([]);
    setChatDrawerOpen(false);
  };

  const handleResumeMemory = (memory) => {
    setShowMemoryDialog(false);
    handleInitialSearch(memory.text);
  };

  const handleStartFresh = () => {
    setShowMemoryDialog(false);
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
        <div className="card-section full">
          <DisplayCards theme={theme} properties={properties} />
        </div>

        <ResumeMemoryDialog
          open={showMemoryDialog}
          onClose={() => setShowMemoryDialog(false)}
          memories={savedMemories}
          onSelectMemory={handleResumeMemory}
          onStartFresh={handleStartFresh}
        />

        <LoginDialog
          open={showLogin}
          onClose={() => setShowLogin(false)}
          setIsLoggedIn={setIsLoggedIn}
          setUserData={setUserData}
          onLoginSuccess={fetchMemories}
        />

        <SignupDialog
          open={showSignup}
          onClose={() => setShowSignup(false)}
          setIsLoggedIn={setIsLoggedIn}
          setUserData={setUserData}
          onSignupSuccess={fetchMemories}
        />

        <ChatDrawer
          open={chatDrawerOpen}
          onClose={() => setChatDrawerOpen(false)}
          chatHistory={chatHistory}
          setChatHistory={setChatHistory}
          setProperties={setProperties}
          setWaitingResponse={setWaitingResponse}
          waitingResponse={waitingResponse}
          checkTokenValidity={checkTokenValidity}
        />

        {!chatDrawerOpen && (
          <Fab
            color="primary"
            aria-label="chat"
            onClick={() => setChatDrawerOpen(true)}
            sx={{
              position: "fixed",
              bottom: 16,
              right: 16,
              backgroundColor: "#157c63",
            }}
          >
            <SmartToyIcon />
          </Fab>
        )}
      </div>
    </ThemeProvider>
  );
}

export default App;
