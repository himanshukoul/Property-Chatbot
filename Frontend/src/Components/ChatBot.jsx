import { useEffect } from "react";
import ChatWindow from "./ChatWindow.jsx";
import ChatQuery from "./ChatQuery.jsx";
import socket from "../static/socket.js";
import { v4 as uuidv4 } from "uuid";
function ChatBot({
  chatHistory,
  setChatHistory,
  setWaitingResponse,
  waitingResponse,
  checkTokenValidity,
}) {
  const handleSendMessage = (message) => {
    if (!checkTokenValidity()) {
      setChatHistory((prev) => [
        ...prev,
        { id: uuidv4(), sender: "bot", message: "Please log in to continue." },
      ]);
      return;
    }
    const token = localStorage.getItem("token");
    socket.auth = { token };
    socket.emit("message", { msg: message });
    setWaitingResponse(true);
    setChatHistory((prev) => [
      ...prev,
      { id: uuidv4(), sender: "user", message },
    ]);
  };
  return (
    <>
      <ChatWindow chatHistory={chatHistory} waitingResponse={waitingResponse} />
      <ChatQuery handleSendMessage={handleSendMessage} />
    </>
  );
}

export default ChatBot;
