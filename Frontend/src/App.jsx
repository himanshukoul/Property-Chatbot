import "./App.css";
import { useState } from "react";
import Navbar from "./Components/Navbar.jsx";
import SearchBar from "./Components/SearchBar.jsx";
import ChatBot from "./Components/ChatBot.jsx";
import DisplayCards from "./Components/DisplayCards.jsx";
import socket from "./static/socket.js";

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
  const handleInitialSearch = (query) => {
    console.log("Init search");
    socket.emit("message", { msg: query });
    console.log("emitted msg", query);
    setWaitingResponse(true);
    setChatHistory((prev) => [...prev, { sender: "user", message: query }]);
    setChatStarted(true);
  };

  return (
    <ThemeProvider theme={theme}>
      <Navbar />
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
            />
          </div>
        )}
      </div>
    </ThemeProvider>
  );
}

export default App;
