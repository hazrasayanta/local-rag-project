import { useState, useEffect, useRef } from "react";
import { Container, TextField, Button, Typography, Paper, CircularProgress, Box } from "@mui/material";
import { motion } from "framer-motion";

function App() {
  const [query, setQuery] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatContainerRef = useRef(null);

  useEffect(() => {
    // Auto-scroll to bottom when a new message appears
    chatContainerRef.current?.scrollTo({ top: chatContainerRef.current.scrollHeight, behavior: "smooth" });
  }, [chatHistory]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    const newUserMessage = { sender: "user", text: query, timestamp: new Date().toLocaleTimeString() };
    setChatHistory((prev) => [...prev, newUserMessage]);

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/rag-query/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, top_k: 3, max_tokens: 128 }),
      });

      const reader = response.body.getReader();
      let botResponse = "";
      setChatHistory((prev) => [...prev, { sender: "bot", text: "", timestamp: new Date().toLocaleTimeString() }]);

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        botResponse += new TextDecoder().decode(value);

        setChatHistory((prev) => [
          ...prev.slice(0, -1),
          { sender: "bot", text: botResponse, timestamp: new Date().toLocaleTimeString() },
        ]);
      }
    } catch (error) {
      setChatHistory((prev) => [...prev, { sender: "bot", text: "Error fetching response.", timestamp: new Date().toLocaleTimeString() }]);
    }

    setQuery("");
    setLoading(false);
  };

  return (
    <Container maxWidth="md" sx={{ mt: 5, display: "flex", flexDirection: "column", height: "90vh" }}>
      <Typography variant="h4" align="center" gutterBottom>
        Local RAG Chat
      </Typography>
      
      <Paper ref={chatContainerRef} sx={{ flexGrow: 1, overflowY: "auto", p: 2, maxHeight: "70vh", display: "flex", flexDirection: "column" }}>
        {chatHistory.map((msg, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            style={{
              display: "flex",
              justifyContent: msg.sender === "user" ? "flex-end" : "flex-start",
            }}
          >
            <Box
              sx={{
                bgcolor: msg.sender === "user" ? "#1976d2" : "#e0e0e0",
                color: msg.sender === "user" ? "white" : "black",
                p: 1.5,
                borderRadius: 2,
                mb: 1,
                maxWidth: "75%",
                boxShadow: 2,
              }}
            >
              <Typography sx={{ fontSize: 12, opacity: 0.7 }}>
                {msg.sender === "user" ? "You" : "Bot"} • {msg.timestamp}
              </Typography>
              <Typography>{msg.text}</Typography>
            </Box>
          </motion.div>
        ))}
      </Paper>

      <form onSubmit={handleSubmit} style={{ display: "flex", marginTop: "10px" }}>
        <TextField
          variant="outlined"
          fullWidth
          placeholder="Type a message..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <Button type="submit" variant="contained" color="primary" disabled={loading} sx={{ ml: 1 }}>
          {loading ? <CircularProgress size={24} /> : "Send"}
        </Button>
      </form>
    </Container>
  );
}

export default App;
