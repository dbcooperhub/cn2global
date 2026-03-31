const express = require('express');
const mysql = require('mysql2/promise');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'cn2global-secret-2024';

app.use(cors());
app.use(express.json());

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'Asd1988.',
  database: 'cn2global',
  waitForConnections: true,
  connectionLimit: 10
});

// Auth middleware
const auth = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ success: false, message: 'No token' });
  try {
    req.userId = jwt.verify(token, JWT_SECRET).userId;
    next();
  } catch (e) {
    res.status(401).json({ success: false, message: 'Invalid token' });
  }
};

// Register
app.post('/api/auth/register', async (req, res) => {
  const { phone, country_code, email, password, name } = req.body;
  try {
    const hash = await bcrypt.hash(password, 10);
    const fullPhone = country_code ? `${country_code}${phone}` : phone;
    const [r] = await pool.execute(
      'INSERT INTO users (phone, email, password, name, country_code) VALUES (?, ?, ?, ?, ?)',
      [fullPhone, email || null, hash, name || null, country_code || null]
    );
    const token = jwt.sign({ userId: r.insertId }, JWT_SECRET, { expiresIn: '7d' });
    res.json({ success: true, data: { userId: r.insertId, token } });
  } catch (e) {
    if (e.code === 'ER_DUP_ENTRY') return res.status(400).json({ success: false, message: 'Phone or email exists' });
    res.status(500).json({ success: false, message: 'Register failed' });
  }
});

// Login
app.post('/api/auth/login', async (req, res) => {
  const { account, password } = req.body;
  try {
    const [users] = await pool.execute('SELECT * FROM users WHERE phone = ? OR email = ?', [account, account]);
    if (!users.length) return res.status(401).json({ success: false, message: 'Not found' });
    const user = users[0];
    if (!user.password) return res.status(400).json({ success: false, message: 'Use Google login' });
    if (!await bcrypt.compare(password, user.password)) return res.status(401).json({ success: false, message: 'Wrong password' });
    const token = jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '7d' });
    res.json({ success: true, data: { token, name: user.name, email: user.email } });
  } catch (e) {
    res.status(500).json({ success: false, message: 'Login failed' });
  }
});

// Google Login
app.post('/api/auth/google', async (req, res) => {
  const { google_id, email, name, picture } = req.body;
  try {
    const [users] = await pool.execute('SELECT * FROM users WHERE email = ? OR google_id = ?', [email, google_id]);
    let user;
    if (users.length) {
      user = users[0];
      if (!user.google_id) await pool.execute('UPDATE users SET google_id = ? WHERE id = ?', [google_id, user.id]);
    } else {
      const [r] = await pool.execute('INSERT INTO users (email, name, google_id, avatar) VALUES (?, ?, ?, ?)', [email, name, google_id, picture]);
      user = { id: r.insertId, name, email };
    }
    const token = jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '7d' });
    res.json({ success: true, data: { token, name: user.name, email: user.email, isNewUser: !users.length } });
  } catch (e) {
    res.status(500).json({ success: false, message: 'Google login failed' });
  }
});

// Get user info
app.get('/api/auth/me', auth, async (req, res) => {
  const [users] = await pool.execute('SELECT id, phone, email, name, country_code, member_level FROM users WHERE id = ?', [req.userId]);
  res.json({ success: true, data: users[0] });
});

// Update phone
app.put('/api/auth/phone', auth, async (req, res) => {
  const { phone, country_code } = req.body;
  const fullPhone = `${country_code}${phone}`;
  await pool.execute('UPDATE users SET phone = ?, country_code = ? WHERE id = ?', [fullPhone, country_code, req.userId]);
  res.json({ success: true });
});

// Calculate shipping
app.post('/api/calculate', async (req, res) => {
  const { country_code, weight, method } = req.body;
  const [rates] = await pool.execute('SELECT * FROM shipping_rates WHERE country_code = ?', [country_code]);
  if (!rates.length) return res.status(404).json({ success: false, message: 'Country not found' });
  const r = rates[0];
  const baseFee = weight * parseFloat(r[method + '_rate']);
  const total = baseFee + 30;
  res.json({ success: true, data: { baseFee: baseFee.toFixed(2), totalFee: total.toFixed(2), days: r[method + '_days'] } });
});

// Get rates
app.get('/api/rates', async (req, res) => {
  const [rates] = await pool.execute('SELECT * FROM shipping_rates ORDER BY country_name_en');
  res.json({ success: true, data: rates });
});

// Addresses
app.get('/api/addresses', auth, async (req, res) => {
  const [addr] = await pool.execute('SELECT * FROM addresses WHERE user_id = ?', [req.userId]);
  res.json({ success: true, data: addr });
});

app.post('/api/addresses', auth, async (req, res) => {
  const { country, state, city, street, zip_code, contact_name, contact_phone, is_default } = req.body;
  if (is_default) await pool.execute('UPDATE addresses SET is_default = 0 WHERE user_id = ?', [req.userId]);
  const [r] = await pool.execute(
    'INSERT INTO addresses (user_id, country, state, city, street, zip_code, contact_name, contact_phone, is_default) VALUES (?,?,?,?,?,?,?,?,?)',
    [req.userId, country, state, city, street, zip_code, contact_name, contact_phone, is_default || 0]
  );
  res.json({ success: true, data: { id: r.insertId } });
});

// Packages
app.get('/api/packages', auth, async (req, res) => {
  const [pkg] = await pool.execute('SELECT * FROM packages WHERE user_id = ? ORDER BY created_at DESC', [req.userId]);
  res.json({ success: true, data: pkg });
});

app.post('/api/packages/forecast', auth, async (req, res) => {
  const { tracking_number, name, estimated_weight } = req.body;
  const code = 'CN2G' + req.userId.toString().padStart(6, '0');
  const [r] = await pool.execute(
    'INSERT INTO packages (user_id, tracking_number, warehouse_code, name, estimated_weight) VALUES (?,?,?,?,?)',
    [req.userId, tracking_number, code, name, estimated_weight]
  );
  res.json({ success: true, data: { id: r.insertId } });
});

// Warehouse
app.get('/api/warehouse', auth, async (req, res) => {
  res.json({
    success: true,
    data: {
      code: 'CN2G' + req.userId.toString().padStart(6, '0'),
      address: 'Qingdao, Shandong, China',
      address_zh: '山东省青岛市市北区',
      address_ko: '중국 산둥성 칭다오시',
      phone: '400-888-8888'
    }
  });
});

// Orders
app.get('/api/orders', auth, async (req, res) => {
  const [orders] = await pool.execute('SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC', [req.userId]);
  res.json({ success: true, data: orders });
});

app.listen(PORT, '0.0.0.0', () => console.log(`API running on ${PORT}`));
