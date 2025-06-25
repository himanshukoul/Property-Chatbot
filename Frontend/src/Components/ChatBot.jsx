import { useEffect } from "react";
import ChatWindow from "./ChatWindow.jsx";
import ChatQuery from "./ChatQuery.jsx";
import socket from "../static/socket.js";

function ChatBot({
  chatHistory,
  setChatHistory,
  setProperties,
  setWaitingResponse,
  waitingResponse,
}) {
  useEffect(() => {
    socket.on("bot_response", (data) => {
      setWaitingResponse(false);
      if (data.message) {
        setChatHistory((prev) => [
          ...prev,
          { sender: "bot", message: data.message },
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

  const handleSendMessage = (message) => {
    socket.emit("message", { msg: message });
    setWaitingResponse(true);
    setChatHistory((prev) => [...prev, { sender: "user", message }]);
  };
  return (
    <>
      <ChatWindow chatHistory={chatHistory} waitingResponse={waitingResponse} />
      <ChatQuery handleSendMessage={handleSendMessage} />
    </>
  );
}

export default ChatBot;
