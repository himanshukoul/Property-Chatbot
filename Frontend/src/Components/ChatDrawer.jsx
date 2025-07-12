import { Drawer, Box } from "@mui/material";
import ChatWindow from "./ChatWindow";
import ChatQuery from "./ChatQuery";
import socket from "../static/socket";
import { v4 as uuidv4 } from "uuid";

function ChatDrawer({
  open,
  onClose,
  chatHistory,
  setChatHistory,
  setProperties,
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
    <Drawer anchor="right" open={open} onClose={onClose}>
      <Box
        sx={{
          width: { xs: 300, sm: 400 },
          height: "100%",
          display: "flex",
          flexDirection: "column",
          backgroundColor: "whitesmoke",
        }}
      >
        <ChatWindow
          chatHistory={chatHistory}
          waitingResponse={waitingResponse}
        />
        <ChatQuery handleSendMessage={handleSendMessage} />
      </Box>
    </Drawer>
  );
}

export default ChatDrawer;
