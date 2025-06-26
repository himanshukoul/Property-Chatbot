import CircularProgress from "@mui/material/CircularProgress";
function ChatWindow({ chatHistory, waitingResponse }) {
  return (
    <div className="chat-window">
      {chatHistory.map((msg, index) => (
        <div
          key={msg.id} 
          className={
            msg.sender === "user" ? "chat-bubble user" : "chat-bubble bot"
          }
        >
          {msg.message}
        </div>
      ))}
      &nbsp; &nbsp; &nbsp;
      {waitingResponse && (
        <CircularProgress size="30px" sx={{ color: "#FF7300" }} />
      )}
    </div>
  );
}

export default ChatWindow;
