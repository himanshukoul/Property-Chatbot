import { Box, TextField, IconButton } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import { useState } from "react";

function ChatQuery({ handleSendMessage }) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    handleSendMessage(input.trim());
    setInput("");
  };

  return (
    <Box sx={{ display: "flex", p: 1, borderTop: "1px solid #ccc" }}>
      <TextField
        fullWidth
        variant="outlined"
        placeholder="Ask about properties..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
      />
      <IconButton color="primary" onClick={handleSend}>
        <SendIcon />
      </IconButton>
    </Box>
  );
}

export default ChatQuery;
