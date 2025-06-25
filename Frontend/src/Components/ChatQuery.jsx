import { useState } from "react";

function ChatQuery({ handleSendMessage }) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    handleSendMessage(input.trim());
    setInput("");
  };

  return (
    <div className="chat-query">
      <input
        type="text"
        placeholder="Ask about properties..."
        value={input}
        onChange={(event) => setInput(event.target.value)}
        onKeyDown={(event) => event.key === "Enter" && handleSend()}
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}

export default ChatQuery;
