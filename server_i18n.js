const express = require('express');
const mysql = require('mysql2/promise');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const { body, validationResult } = require('express-validator');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'cn2global-secret-key-2024';
const GOOGLE_CLIENT_ID = process.env.GOOGLE_CLIENT_ID || '';
const GOOGLE_CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET || '';
const GOOGLE_REDIRECT_URI = process.env.GOOGLE_REDIRECT_URI || 'http://localhost:3000/api/auth/google/callback';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Database connection pool
const pool = mysql.createPool({
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || 'Asd1988.',
  database: process.env.DB_NAME || 'cn2global',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

// ==================== DATABASE INITIALIZATION ====================
async function initDatabase() {
  const conn = await pool.getConnection();
  
  try {
    // Users table - 添加国际化字段
    await conn.execute(`
      CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        phone VARCHAR(20) UNIQUE,
        email VARCHAR(100) UNIQUE,
        password VARCHAR(255),
        name VARCHAR(100),
        country VARCHAR(10),
        language VARCHAR(10) DEFAULT 'en',
        google_id VARCHAR(255) UNIQUE,
        member_level ENUM('normal', 'silver', 'gold', 'diamond') DEFAULT 'normal',
        points INT DEFAULT 0,
        balance DECIMAL(10,2) DEFAULT 0.00,
        phone_verified BOOLEAN DEFAULT FALSE,
        email_verified BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_phone (phone),
        INDEX idx_email (email),
        INDEX idx_google_id (google_id)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    `);

    // Verification codes table
    await conn.execute(`
      CREATE TABLE IF NOT EXISTS verification_codes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        phone VARCHAR(20) NOT NULL,
        code VARCHAR(6) NOT NULL,
        attempts INT DEFAULT 0,
        expires_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_phone (phone)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    `);

    // Addresses table
    await conn.execute(`
      CREATE TABLE IF NOT EXISTS addresses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        country VARCHAR(50) NOT NULL,
        state VARCHAR(50),
        city VARCHAR(50) NOT NULL,
        street VARCHAR(255) NOT NULL,
        zip_code VARCHAR(20),
        contact_name VARCHAR(100) NOT NULL,
        contact_phone VARCHAR(20),
        is_default BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    `);

    // Packages table
    await conn.execute(`
      CREATE TABLE IF NOT EXISTS packages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        tracking_number VARCHAR(100) NOT NULL UNIQUE,
        warehouse_code VARCHAR(50),
        name VARCHAR(255),
        estimated_weight DECIMAL(10,2),
        actual_weight DECIMAL(10,2),
        volume DECIMAL(10,2),
        status ENUM('pending', 'received', 'verified', 'packed', 'shipped', 'delivered') DEFAULT 'pending',
        photos JSON,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        INDEX idx_user_id (user_id)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    `);

    // Orders table
    await conn.execute(`
      CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_number VARCHAR(50) NOT NULL UNIQUE,
        user_id INT NOT NULL,
        address_id INT NOT NULL,
        shipping_method ENUM('air', 'sea', 'express', 'line') NOT NULL,
        total_weight DECIMAL(10,2),
        total_volume DECIMAL(10,2),
        total_price DECIMAL(10,2),
        status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (address_id) REFERENCES addresses(id),
        INDEX idx_user_id (user_id)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    `);

    console.log('Database initialized successfully');
  } finally {
    conn.release();
  }
}

// ==================== AUTHENTICATION ROUTES ====================

// 注册 - 手机号
app.post('/api/auth/register', [
  body('country').notEmpty().trim(),
  body('phone').notEmpty().isMobilePhone(),
  body('email').optional().isEmail(),
  body('password').isLength({ min: 8 }),
  body('language').optional().trim()
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  const { country, phone, email, password, language } = req.body;

  try {
    const conn = await pool.getConnection();

    // 检查手机号是否已存在
    const [existing] = await conn.execute('SELECT id FROM users WHERE phone = ?', [phone]);
    if (existing.length > 0) {
      conn.release();
      return res.status(400).json({ message: 'Phone number already registered' });
    }

    // 检查邮箱是否已存在
    if (email) {
      const [existingEmail] = await conn.execute('SELECT id FROM users WHERE email = ?', [email]);
      if (existingEmail.length > 0) {
        conn.release();
        return res.status(400).json({ message: 'Email already registered' });
      }
    }

    // 加密密码
    const hashedPassword = await bcrypt.hash(password, 10);

    // 创建用户
    await conn.execute(
      'INSERT INTO users (phone, email, password, country, language) VALUES (?, ?, ?, ?, ?)',
      [phone, email || null, hashedPassword, country, language || 'en']
    );

    conn.release();

    res.json({ 
      message: 'Registration successful',
      redirect: '/login_i18n.html'
    });
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ message: 'Registration failed' });
  }
});

// 登录 - 手机号 + 密码
app.post('/api/auth/login', [
  body('phone').notEmpty().isMobilePhone(),
  body('password').notEmpty()
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  const { phone, password, language } = req.body;

  try {
    const conn = await pool.getConnection();

    // 查找用户
    const [users] = await conn.execute('SELECT * FROM users WHERE phone = ?', [phone]);
    
    if (users.length === 0) {
      conn.release();
      return res.status(401).json({ message: 'Invalid phone or password' });
    }

    const user = users[0];

    // 验证密码
    const passwordMatch = await bcrypt.compare(password, user.password);
    if (!passwordMatch) {
      conn.release();
      return res.status(401).json({ message: 'Invalid phone or password' });
    }

    // 生成 JWT token
    const token = jwt.sign(
      { id: user.id, phone: user.phone, language: user.language },
      JWT_SECRET,
      { expiresIn: '7d' }
    );

    conn.release();

    res.json({
      token,
      user: {
        id: user.id,
        phone: user.phone,
        email: user.email,
        name: user.name,
        country: user.country,
        language: user.language,
        member_level: user.member_level
      }
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ message: 'Login failed' });
  }
});

// Google OAuth - 重定向到 Google
app.get('/api/auth/google', (req, res) => {
  const scope = 'openid email profile';
  const googleAuthUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${GOOGLE_CLIENT_ID}&redirect_uri=${encodeURIComponent(GOOGLE_REDIRECT_URI)}&response_type=code&scope=${encodeURIComponent(scope)}`;
  res.redirect(googleAuthUrl);
});

// Google OAuth - 回调处理
app.get('/api/auth/google/callback', async (req, res) => {
  const { code, error } = req.query;

  if (error) {
    return res.redirect(`/login_i18n.html?error=${error}`);
  }

  try {
    // 交换 code 获取 token
    const tokenResponse = await axios.post('https://oauth2.googleapis.com/token', {
      client_id: GOOGLE_CLIENT_ID,
      client_secret: GOOGLE_CLIENT_SECRET,
      code,
      grant_type: 'authorization_code',
      redirect_uri: GOOGLE_REDIRECT_URI
    });

    const { access_token } = tokenResponse.data;

    // 获取用户信息
    const userResponse = await axios.get('https://www.googleapis.com/oauth2/v2/userinfo', {
      headers: { Authorization: `Bearer ${access_token}` }
    });

    const { id: googleId, email, name, picture } = userResponse.data;

    const conn = await pool.getConnection();

    // 检查用户是否存在
    let [users] = await conn.execute('SELECT * FROM users WHERE google_id = ?', [googleId]);

    let user;
    if (users.length === 0) {
      // 创建新用户
      await conn.execute(
        'INSERT INTO users (google_id, email, name, email_verified, language) VALUES (?, ?, ?, ?, ?)',
        [googleId, email, name, true, 'en']
      );

      [users] = await conn.execute('SELECT * FROM users WHERE google_id = ?', [googleId]);
      user = users[0];
    } else {
      user = users[0];
    }

    conn.release();

    // 生成 JWT token
    const token = jwt.sign(
      { id: user.id, email: user.email, language: user.language },
      JWT_SECRET,
      { expiresIn: '7d' }
    );

    // 重定向到仪表板，带上 token
    res.redirect(`/dashboard.html?token=${token}`);
  } catch (error) {
    console.error('Google OAuth error:', error);
    res.redirect('/login_i18n.html?error=oauth_failed');
  }
});

// 验证 token 中间件
function verifyToken(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ message: 'No token provided' });
  }

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ message: 'Invalid token' });
  }
}

// 获取用户信息
app.get('/api/user/profile', verifyToken, async (req, res) => {
  try {
    const conn = await pool.getConnection();
    const [users] = await conn.execute('SELECT * FROM users WHERE id = ?', [req.user.id]);
    conn.release();

    if (users.length === 0) {
      return res.status(404).json({ message: 'User not found' });
    }

    const user = users[0];
    res.json({
      id: user.id,
      phone: user.phone,
      email: user.email,
      name: user.name,
      country: user.country,
      language: user.language,
      member_level: user.member_level,
      points: user.points,
      balance: user.balance
    });
  } catch (error) {
    console.error('Profile error:', error);
    res.status(500).json({ message: 'Failed to fetch profile' });
  }
});

// 更新用户语言
app.put('/api/user/language', verifyToken, async (req, res) => {
  const { language } = req.body;

  if (!['en', 'zh', 'ja', 'de', 'fr'].includes(language)) {
    return res.status(400).json({ message: 'Invalid language' });
  }

  try {
    const conn = await pool.getConnection();
    await conn.execute('UPDATE users SET language = ? WHERE id = ?', [language, req.user.id]);
    conn.release();

    res.json({ message: 'Language updated' });
  } catch (error) {
    console.error('Language update error:', error);
    res.status(500).json({ message: 'Failed to update language' });
  }
});

// ==================== CUSTOMER SUPPORT ROUTES ====================

// 获取客服信息（国际化）
app.get('/api/support/info', (req, res) => {
  const language = req.query.lang || 'en';

  const supportInfo = {
    en: {
      title: 'Customer Support',
      channels: [
        { type: 'chat', name: 'Live Chat', available: true, hours: '9:00-18:00 UTC' },
        { type: 'email', name: 'Email', email: 'support@cn2global.com', hours: '24/7' },
        { type: 'phone', name: 'Phone', phone: '+86-532-8888-8888', hours: '9:00-18:00 CST' }
      ]
    },
    zh: {
      title: '客户支持',
      channels: [
        { type: 'chat', name: '在线客服', available: true, hours: '9:00-18:00' },
        { type: 'email', name: '邮件', email: 'support@cn2global.com', hours: '24/7' },
        { type: 'phone', name: '电话', phone: '+86-532-8888-8888', hours: '9:00-18:00' }
      ]
    },
    ja: {
      title: 'カスタマーサポート',
      channels: [
        { type: 'chat', name: 'ライブチャット', available: true, hours: '9:00-18:00' },
        { type: 'email', name: 'メール', email: 'support@cn2global.com', hours: '24/7' },
        { type: 'phone', name: '電話', phone: '+86-532-8888-8888', hours: '9:00-18:00' }
      ]
    },
    de: {
      title: 'Kundensupport',
      channels: [
        { type: 'chat', name: 'Live-Chat', available: true, hours: '9:00-18:00' },
        { type: 'email', name: 'E-Mail', email: 'support@cn2global.com', hours: '24/7' },
        { type: 'phone', name: 'Telefon', phone: '+86-532-8888-8888', hours: '9:00-18:00' }
      ]
    },
    fr: {
      title: 'Support Client',
      channels: [
        { type: 'chat', name: 'Chat en direct', available: true, hours: '9:00-18:00' },
        { type: 'email', name: 'E-mail', email: 'support@cn2global.com', hours: '24/7' },
        { type: 'phone', name: 'Téléphone', phone: '+86-532-8888-8888', hours: '9:00-18:00' }
      ]
    }
  };

  res.json(supportInfo[language] || supportInfo['en']);
});

// 提交客服工单
app.post('/api/support/ticket', verifyToken, [
  body('subject').notEmpty().trim(),
  body('message').notEmpty().trim(),
  body('category').notEmpty().trim()
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  const { subject, message, category } = req.body;

  try {
    const conn = await pool.getConnection();

    // 创建工单
    const ticketNumber = `TK-${Date.now()}`;
    await conn.execute(
      'INSERT INTO support_tickets (ticket_number, user_id, subject, message, category, status) VALUES (?, ?, ?, ?, ?, ?)',
      [ticketNumber, req.user.id, subject, message, category, 'open']
    );

    conn.release();

    res.json({ 
      message: 'Ticket created successfully',
      ticket_number: ticketNumber
    });
  } catch (error) {
    console.error('Ticket creation error:', error);
    res.status(500).json({ message: 'Failed to create ticket' });
  }
});

// ==================== INITIALIZATION & SERVER START ====================

async function startServer() {
  try {
    await initDatabase();
    
    app.listen(PORT, () => {
      console.log(`CN2Global API Server running on port ${PORT}`);
      console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

startServer();

module.exports = app;
