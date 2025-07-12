import { Box, Typography, Paper, CircularProgress } from "@mui/material";

function ChatWindow({ chatHistory, waitingResponse }) {
  return (
    <Box
      sx={{
        height: "90%",
        overflowY: "auto",
        padding: 2,
        display: "flex",
        flexDirection: "column",
        gap: 1,
      }}
    >
      {chatHistory.map((msg) => (
        <Box
          key={msg.id}
          sx={{
            display: "flex",
            justifyContent: msg.sender === "user" ? "flex-end" : "flex-start",
          }}
        >
          <Paper
            elevation={3}
            sx={{
              px: 2,
              py: 1,
              maxWidth: "70%",
              borderRadius: 3,
              backgroundColor: msg.sender === "user" ? "#157c63" : "#1976d2",
              color: "white",
              wordBreak: "break-word",
            }}
          >
            <Typography variant="body1">{msg.message}</Typography>
          </Paper>
        </Box>
      ))}
      {waitingResponse && (
        <Box sx={{ display: "flex", justifyContent: "center", marginTop: 1 }}>
          <CircularProgress size={30} sx={{ color: "#FF7300" }} />
        </Box>
      )}
    </Box>
  );
}

export default ChatWindow;
