const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: process.env.DB_PORT || 3306
});

app.get('/api/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    res.json({ success: true, message: 'Servidor conectado correctamente a MySQL' });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

app.get('/api/tickets', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT * FROM tickets ORDER BY created_at DESC');
    res.json({ success: true, data: rows });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

app.post('/api/tickets', async (req, res) => {
  const { id, requester, email, userType, area, category, location, equipment, priority, technician, status, description, date } = req.body;
  try {
    await pool.query(
      `INSERT INTO tickets (id, requester, email, userType, area, category, location, equipment, priority, technician, status, description, date) 
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      [id, requester, email, userType, area || '', category, location, equipment || '', priority, technician || 'Por asignar', status || 'Nuevo', description, date]
    );
    res.status(201).json({ success: true, message: 'Ticket registrado en MySQL' });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

app.put('/api/tickets/:id', async (req, res) => {
  const { id } = req.params;
  const { status, technician } = req.body;
  try {
    await pool.query(
      'UPDATE tickets SET status = ?, technician = ? WHERE id = ?',
      [status, technician, id]
    );
    res.json({ success: true, message: 'Ticket actualizado' });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`SENA SUPPORT funcionando en http://localhost:${PORT}`);
});
