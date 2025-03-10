const { Pool } = require('pg');

const pool = new Pool({
    user: 'rag_user',
    host: 'localhost',
    database: 'rag_db',
    password: 'rag_password',
    port: 5432, // Default PostgreSQL port
});

async function createTable() {
    try {
        const result = await pool.query(`
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            );
        `);
        console.log("Table created successfully:", result);
    } catch (error) {
        console.error("Error creating table:", error);
    } finally {
        await pool.end(); // Close connection
    }
}

createTable();
