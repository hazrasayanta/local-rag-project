const express = require("express");
const axios = require("axios");
require("dotenv").config();
const pool = require("./db");

const app = express();
app.use(express.json());
app.use(require("cors")());

const PORT = process.env.PORT || 6000;

// Test route
app.get("/", (req, res) => {
  res.json({ message: "Node.js backend is running" });
});

// Example: Fetch data from FastAPI
app.get("/fetch-data", async (req, res) => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/"); // FastAPI endpoint
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: "Error fetching data" });
  }
});

// Example: Fetch data from PostgreSQL
app.get("/test-db", async (req, res) => {
    try {
      const result = await pool.query("SELECT NOW()");
      res.json({ success: true, time: result.rows[0] });
    } catch (error) {
      res.status(500).json({ error: "Database connection failed" });
    }
  });

app.listen(PORT, () => {
  console.log(`Node.js backend running on http://localhost:${PORT}`);
});
