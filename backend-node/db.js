const { Pool } = require("pg");
require("dotenv").config();

const pool = new Pool({
  user: process.env.DB_USER || "rag_user",
  host: process.env.DB_HOST || "localhost",
  database: process.env.DB_NAME || "rag_db",
  password: process.env.DB_PASS || "rag_password",
  port: process.env.DB_PORT || 5432,
  ssl: process.env.DB_SSL ? { rejectUnauthorized: false } : false, // Fix SSL errors
});

pool.connect()
  .then(() => console.log("✅ PostgreSQL Connected"))
  .catch((err) => console.error("❌ Database Connection Error:", err));

module.exports = pool;
