const express = require('express');
const mysql = require('mysql2/promise');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const { body, validationResult } = require('express-validator');
const multer = require('multer');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'cn2global-secret-key-2024';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

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
  
  // Users table
  await conn.execute(`
    CREATE TABLE IF NOT EXISTS users (
      id INT AUTO_INCREMENT PRIMARY KEY,
      phone VARCHAR(20),
      email VARCHAR(100),
      password VARCHAR(255) NOT NULL,
      name VARCHAR(100),
      member_level ENUM('normal', 'silver', 'gold', 'diamond') DEFAULT 'normal',
      points INT DEFAULT 0,
      balance DECIMAL(10,2) DEFAULT 0.00,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      UNIQUE KEY unique_phone (phone),
      UNIQUE KEY unique_email (email)
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
      tracking_number VARCHAR(100) NOT NULL,
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
      FOREIGN KEY (user_id) REFERENCES users(id)
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
      base_fee DECIMAL(10,2),
      service_fee DECIMAL(10,2),
      total_fee DECIMAL(10,2),
      status ENUM('pending_payment', 'pending_pack', 'packed', 'shipped', 'in_transit', 'customs', 'delivered', 'cancelled') DEFAULT 'pending_payment',
      tracking_number VARCHAR(100),
      payment_method VARCHAR(50),
      payment_status ENUM('pending', 'paid', 'refunded') DEFAULT 'pending',
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id),
      FOREIGN KEY (address_id) REFERENCES addresses(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  `);

  // Order items (packages in order)
  await conn.execute(`
    CREATE TABLE IF NOT EXISTS order_items (
      id INT AUTO_INCREMENT PRIMARY KEY,
      order_id INT NOT NULL,
      package_id INT NOT NULL,
      FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
      FOREIGN KEY (package_id) REFERENCES packages(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  `);

  // Tracking history
  await conn.execute(`
    CREATE TABLE IF NOT EXISTS tracking_history (
      id INT AUTO_INCREMENT PRIMARY KEY,
      order_id INT NOT NULL,
      status VARCHAR(50) NOT NULL,
      location VARCHAR(100),
      description TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  `);

  // Coupons
  await conn.execute(`
    CREATE TABLE IF NOT EXISTS coupons (
      id INT AUTO_INCREMENT PRIMARY KEY,
      code VARCHAR(50) NOT NULL UNIQUE,
      type ENUM('discount', 'cash', 'shipping') NOT NULL,
      value DECIMAL(10,2) NOT NULL,
      min_amount DECIMAL(10,2) DEFAULT 0,
      max_uses INT DEFAULT NULL,
      used_count INT DEFAULT 0,
      expires_at TIMESTAMP NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  `);

  // User coupons
  await conn.execute(`
    CREATE TABLE IF NOT EXISTS user_coupons (
      id INT AUTO_INCREMENT PRIMARY KEY,
      user_id INT NOT NULL,
      coupon_id INT NOT NULL,
      used BOOLEAN DEFAULT FALSE,
      used_at TIMESTAMP NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id),
      FOREIGN KEY (coupon_id) REFERENCES coupons(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  `);

  // Notifications
  await conn.execute(`
    CREATE TABLE IF NOT EXISTS notifications (
      id INT AUTO_INCREMENT PRIMARY KEY,
      user_id INT NOT NULL,
      type VARCHAR(50) NOT NULL,
      title VARCHAR(255) NOT NULL,
      content TEXT,
      is_read BOOLEAN DEFAULT FALSE,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  `);

  // Shipping rates
  await conn.execute(`
    CREATE TABLE IF NOT EXISTS shipping_rates (
      id INT AUTO_INCREMENT PRIMARY KEY,
      country_code VARCHAR(10) NOT NULL,
      country_name_en VARCHAR(100) NOT NULL,
      country_name_zh VARCHAR(100) NOT NULL,
      air_rate DECIMAL(10,2) NOT NULL,
      sea_rate DECIMAL(10,2) NOT NULL,
      express_rate DECIMAL(10,2) NOT NULL,
      line_rate DECIMAL(10,2),
      air_days VARCHAR(20),
      sea_days VARCHAR(20),
      express_days VARCHAR(20),
      line_days VARCHAR(20),
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      UNIQUE KEY unique_country (country_code)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  `);

  conn.release();
  console.log('✅ Database tables initialized');
}

// ==================== AUTH MIDDLEWARE ====================
const authMiddleware = async (req, res, next) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) {
      return res.status(401).json({ success: false, message: 'No token provided' });
    }
    const decoded = jwt.verify(token, JWT_SECRET);
    req.userId = decoded.userId;
    next();
  } catch (error) {
    res.status(401).json({ success: false, message: 'Invalid token' });
  }
};

// ==================== AUTH ROUTES ====================

// Register
app.post('/api/auth/register',
  [
    body('phone').optional().isMobilePhone(),
    body('email').optional().isEmail(),
    body('password').isLength({ min: 6 })
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ success: false, errors: errors.array() });
      }

      const { phone, email, password, name } = req.body;
      
      if (!phone && !email) {
        return res.status(400).json({ success: false, message: 'Phone or email required' });
      }

      const hashedPassword = await bcrypt.hash(password, 10);
      
      // Generate unique warehouse code
      const warehouseCode = 'CN2G' + Date.now().toString(36).toUpperCase();

      const [result] = await pool.execute(
        'INSERT INTO users (phone, email, password, name) VALUES (?, ?, ?, ?)',
        [phone || null, email || null, hashedPassword, name || null]
      );

      const token = jwt.sign({ userId: result.insertId }, JWT_SECRET, { expiresIn: '7d' });

      res.json({
        success: true,
        message: 'Registration successful',
        data: {
          userId: result.insertId,
          token,
          warehouseCode
        }
      });
    } catch (error) {
      if (error.code === 'ER_DUP_ENTRY') {
        return res.status(400).json({ success: false, message: 'Phone or email already registered' });
      }
      console.error('Register error:', error);
      res.status(500).json({ success: false, message: 'Registration failed' });
    }
  }
);

// Login
app.post('/api/auth/login', async (req, res) => {
  try {
    const { account, password } = req.body; // account can be phone or email

    const [users] = await pool.execute(
      'SELECT * FROM users WHERE phone = ? OR email = ?',
      [account, account]
    );

    if (users.length === 0) {
      return res.status(401).json({ success: false, message: 'Account not found' });
    }

    const user = users[0];
    const isValid = await bcrypt.compare(password, user.password);

    if (!isValid) {
      return res.status(401).json({ success: false, message: 'Invalid password' });
    }

    const token = jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '7d' });

    res.json({
      success: true,
      message: 'Login successful',
      data: {
        userId: user.id,
        token,
        name: user.name,
        memberLevel: user.member_level,
        points: user.points,
        balance: user.balance
      }
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ success: false, message: 'Login failed' });
  }
});

// Get current user
app.get('/api/auth/me', authMiddleware, async (req, res) => {
  try {
    const [users] = await pool.execute(
      'SELECT id, phone, email, name, member_level, points, balance, created_at FROM users WHERE id = ?',
      [req.userId]
    );

    if (users.length === 0) {
      return res.status(404).json({ success: false, message: 'User not found' });
    }

    res.json({ success: true, data: users[0] });
  } catch (error) {
    console.error('Get user error:', error);
    res.status(500).json({ success: false, message: 'Failed to get user info' });
  }
});

// ==================== ADDRESS ROUTES ====================

// Get addresses
app.get('/api/addresses', authMiddleware, async (req, res) => {
  try {
    const [addresses] = await pool.execute(
      'SELECT * FROM addresses WHERE user_id = ? ORDER BY is_default DESC, created_at DESC',
      [req.userId]
    );
    res.json({ success: true, data: addresses });
  } catch (error) {
    console.error('Get addresses error:', error);
    res.status(500).json({ success: false, message: 'Failed to get addresses' });
  }
});

// Add address
app.post('/api/addresses', authMiddleware, async (req, res) => {
  try {
    const { country, state, city, street, zip_code, contact_name, contact_phone, is_default } = req.body;

    // If default, unset other defaults
    if (is_default) {
      await pool.execute('UPDATE addresses SET is_default = FALSE WHERE user_id = ?', [req.userId]);
    }

    const [result] = await pool.execute(
      'INSERT INTO addresses (user_id, country, state, city, street, zip_code, contact_name, contact_phone, is_default) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
      [req.userId, country, state, city, street, zip_code, contact_name, contact_phone, is_default || false]
    );

    res.json({ success: true, message: 'Address added', data: { addressId: result.insertId } });
  } catch (error) {
    console.error('Add address error:', error);
    res.status(500).json({ success: false, message: 'Failed to add address' });
  }
});

// Update address
app.put('/api/addresses/:id', authMiddleware, async (req, res) => {
  try {
    const { country, state, city, street, zip_code, contact_name, contact_phone, is_default } = req.body;

    if (is_default) {
      await pool.execute('UPDATE addresses SET is_default = FALSE WHERE user_id = ?', [req.userId]);
    }

    await pool.execute(
      'UPDATE addresses SET country=?, state=?, city=?, street=?, zip_code=?, contact_name=?, contact_phone=?, is_default=? WHERE id=? AND user_id=?',
      [country, state, city, street, zip_code, contact_name, contact_phone, is_default, req.params.id, req.userId]
    );

    res.json({ success: true, message: 'Address updated' });
  } catch (error) {
    console.error('Update address error:', error);
    res.status(500).json({ success: false, message: 'Failed to update address' });
  }
});

// Delete address
app.delete('/api/addresses/:id', authMiddleware, async (req, res) => {
  try {
    await pool.execute('DELETE FROM addresses WHERE id = ? AND user_id = ?', [req.params.id, req.userId]);
    res.json({ success: true, message: 'Address deleted' });
  } catch (error) {
    console.error('Delete address error:', error);
    res.status(500).json({ success: false, message: 'Failed to delete address' });
  }
});

// ==================== PACKAGE ROUTES ====================

// Get warehouse info
app.get('/api/warehouse/info', authMiddleware, async (req, res) => {
  try {
    const warehouseCode = 'CN2G' + req.userId.toString().padStart(6, '0');
    res.json({
      success: true,
      data: {
        code: warehouseCode,
        address: '山东省青岛市市北区延安三路168号',
        recipient: warehouseCode,
        phone: '400-888-8888',
        postalCode: '266000'
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, message: 'Failed to get warehouse info' });
  }
});

// Get packages
app.get('/api/packages', authMiddleware, async (req, res) => {
  try {
    const { status } = req.query;
    let sql = 'SELECT * FROM packages WHERE user_id = ?';
    const params = [req.userId];

    if (status) {
      sql += ' AND status = ?';
      params.push(status);
    }

    sql += ' ORDER BY created_at DESC';

    const [packages] = await pool.execute(sql, params);
    res.json({ success: true, data: packages });
  } catch (error) {
    console.error('Get packages error:', error);
    res.status(500).json({ success: false, message: 'Failed to get packages' });
  }
});

// Submit package forecast
app.post('/api/packages/forecast', authMiddleware, async (req, res) => {
  try {
    const { tracking_number, name, estimated_weight } = req.body;
    const warehouseCode = 'CN2G' + req.userId.toString().padStart(6, '0');

    const [result] = await pool.execute(
      'INSERT INTO packages (user_id, tracking_number, warehouse_code, name, estimated_weight, status) VALUES (?, ?, ?, ?, ?, "pending")',
      [req.userId, tracking_number, warehouseCode, name, estimated_weight]
    );

    res.json({
      success: true,
      message: 'Package forecast submitted',
      data: { packageId: result.insertId }
    });
  } catch (error) {
    console.error('Forecast error:', error);
    res.status(500).json({ success: false, message: 'Failed to submit forecast' });
  }
});

// Batch forecast
app.post('/api/packages/forecast/batch', authMiddleware, async (req, res) => {
  try {
    const { packages } = req.body; // Array of {tracking_number, name, estimated_weight}
    const warehouseCode = 'CN2G' + req.userId.toString().padStart(6, '0');

    const values = packages.map(p => [req.userId, p.tracking_number, warehouseCode, p.name, p.estimated_weight, 'pending']);
    
    const [result] = await pool.execute(
      'INSERT INTO packages (user_id, tracking_number, warehouse_code, name, estimated_weight, status) VALUES ?',
      [values]
    );

    res.json({
      success: true,
      message: `${result.affectedRows} packages forecasted`,
      data: { count: result.affectedRows }
    });
  } catch (error) {
    console.error('Batch forecast error:', error);
    res.status(500).json({ success: false, message: 'Failed to submit batch forecast' });
  }
});

// ==================== SHIPPING RATES ====================

// Get shipping rates
app.get('/api/rates', async (req, res) => {
  try {
    const [rates] = await pool.execute('SELECT * FROM shipping_rates ORDER BY country_name_en');
    res.json({ success: true, data: rates });
  } catch (error) {
    console.error('Get rates error:', error);
    res.status(500).json({ success: false, message: 'Failed to get rates' });
  }
});

// Calculate shipping cost
app.post('/api/calculate', async (req, res) => {
  try {
    const { country_code, weight, method } = req.body;

    const [rates] = await pool.execute(
      'SELECT * FROM shipping_rates WHERE country_code = ?',
      [country_code]
    );

    if (rates.length === 0) {
      return res.status(404).json({ success: false, message: 'Country not found' });
    }

    const rate = rates[0];
    const rateField = method + '_rate';
    const daysField = method + '_days';

    const baseFee = weight * rate[rateField];
    const handlingFee = 30; // CNY handling fee
    const totalFee = baseFee + handlingFee;

    res.json({
      success: true,
      data: {
        baseFee: baseFee.toFixed(2),
        handlingFee: handlingFee.toFixed(2),
        totalFee: totalFee.toFixed(2),
        currency: 'CNY',
        estimatedDays: rate[daysField],
        ratePerKg: rate[rateField]
      }
    });
  } catch (error) {
    console.error('Calculate error:', error);
    res.status(500).json({ success: false, message: 'Calculation failed' });
  }
});

// ==================== ORDER ROUTES ====================

// Create order
app.post('/api/orders', authMiddleware, async (req, res) => {
  const conn = await pool.getConnection();
  try {
    await conn.beginTransaction();

    const { address_id, package_ids, shipping_method, service_options } = req.body;

    // Generate order number
    const orderNumber = 'ORD' + Date.now().toString(36).toUpperCase();

    // Get packages total weight
    const [packages] = await conn.execute(
      'SELECT SUM(actual_weight) as total_weight FROM packages WHERE id IN (?) AND user_id = ?',
      [package_ids, req.userId]
    );

    const totalWeight = packages[0].total_weight || 0;

    // Get rate
    const [addrResult] = await conn.execute('SELECT country FROM addresses WHERE id = ?', [address_id]);
    const countryCode = addrResult[0]?.country;

    const [rates] = await conn.execute('SELECT * FROM shipping_rates WHERE country_code = ?', [countryCode]);
    const rate = rates[0];
    const rateField = shipping_method + '_rate';

    const baseFee = totalWeight * rate[rateField];
    const handlingFee = 30;
    const serviceFee = service_options?.reduce((sum, opt) => sum + opt.price, 0) || 0;
    const totalFee = baseFee + handlingFee + serviceFee;

    // Create order
    const [orderResult] = await conn.execute(
      'INSERT INTO orders (order_number, user_id, address_id, shipping_method, total_weight, base_fee, service_fee, total_fee, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, "pending_payment")',
      [orderNumber, req.userId, address_id, shipping_method, totalWeight, baseFee, serviceFee, totalFee]
    );

    const orderId = orderResult.insertId;

    // Link packages to order
    const orderItems = package_ids.map(pid => [orderId, pid]);
    await conn.execute('INSERT INTO order_items (order_id, package_id) VALUES ?', [orderItems]);

    // Add initial tracking
    await conn.execute(
      'INSERT INTO tracking_history (order_id, status, location, description) VALUES (?, "order_created", "Qingdao, China", "Order created, pending payment")',
      [orderId]
    );

    await conn.commit();

    res.json({
      success: true,
      message: 'Order created',
      data: {
        orderId,
        orderNumber,
        totalFee: totalFee.toFixed(2)
      }
    });
  } catch (error) {
    await conn.rollback();
    console.error('Create order error:', error);
    res.status(500).json({ success: false, message: 'Failed to create order' });
  } finally {
    conn.release();
  }
});

// Get orders
app.get('/api/orders', authMiddleware, async (req, res) => {
  try {
    const { status } = req.query;
    let sql = `
      SELECT o.*, a.country, a.city, a.contact_name 
      FROM orders o 
      LEFT JOIN addresses a ON o.address_id = a.id 
      WHERE o.user_id = ?
    `;
    const params = [req.userId];

    if (status) {
      sql += ' AND o.status = ?';
      params.push(status);
    }

    sql += ' ORDER BY o.created_at DESC';

    const [orders] = await pool.execute(sql, params);
    res.json({ success: true, data: orders });
  } catch (error) {
    console.error('Get orders error:', error);
    res.status(500).json({ success: false, message: 'Failed to get orders' });
  }
});

// Get order detail
app.get('/api/orders/:id', authMiddleware, async (req, res) => {
  try {
    const [orders] = await pool.execute(`
      SELECT o.*, a.* 
      FROM orders o 
      LEFT JOIN addresses a ON o.address_id = a.id 
      WHERE o.id = ? AND o.user_id = ?
    `, [req.params.id, req.userId]);

    if (orders.length === 0) {
      return res.status(404).json({ success: false, message: 'Order not found' });
    }

    const order = orders[0];

    // Get packages
    const [packages] = await pool.execute(`
      SELECT p.* FROM packages p
      JOIN order_items oi ON p.id = oi.package_id
      WHERE oi.order_id = ?
    `, [req.params.id]);

    // Get tracking
    const [tracking] = await pool.execute(
      'SELECT * FROM tracking_history WHERE order_id = ? ORDER BY created_at DESC',
      [req.params.id]
    );

    res.json({
      success: true,
      data: { ...order, packages, tracking }
    });
  } catch (error) {
    console.error('Get order error:', error);
    res.status(500).json({ success: false, message: 'Failed to get order' });
  }
});

// Track by order number (public)
app.get('/api/track/:orderNumber', async (req, res) => {
  try {
    const [orders] = await pool.execute(
      'SELECT * FROM orders WHERE order_number = ?',
      [req.params.orderNumber]
    );

    if (orders.length === 0) {
      return res.status(404).json({ success: false, message: 'Order not found' });
    }

    const [tracking] = await pool.execute(
      'SELECT * FROM tracking_history WHERE order_id = ? ORDER BY created_at DESC',
      [orders[0].id]
    );

    res.json({
      success: true,
      data: {
        order: orders[0],
        tracking
      }
    });
  } catch (error) {
    console.error('Track error:', error);
    res.status(500).json({ success: false, message: 'Tracking failed' });
  }
});

// ==================== COUPON ROUTES ====================

// Get available coupons
app.get('/api/coupons', authMiddleware, async (req, res) => {
  try {
    const [coupons] = await pool.execute(`
      SELECT c.*, uc.id as user_coupon_id, uc.used
      FROM coupons c
      LEFT JOIN user_coupons uc ON c.id = uc.coupon_id AND uc.user_id = ?
      WHERE c.expires_at IS NULL OR c.expires_at > NOW()
      ORDER BY c.created_at DESC
    `, [req.userId]);

    res.json({ success: true, data: coupons });
  } catch (error) {
    console.error('Get coupons error:', error);
    res.status(500).json({ success: false, message: 'Failed to get coupons' });
  }
});

// ==================== NOTIFICATION ROUTES ====================

app.get('/api/notifications', authMiddleware, async (req, res) => {
  try {
    const [notifications] = await pool.execute(
      'SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC LIMIT 50',
      [req.userId]
    );
    res.json({ success: true, data: notifications });
  } catch (error) {
    res.status(500).json({ success: false, message: 'Failed to get notifications' });
  }
});

app.put('/api/notifications/:id/read', authMiddleware, async (req, res) => {
  try {
    await pool.execute(
      'UPDATE notifications SET is_read = TRUE WHERE id = ? AND user_id = ?',
      [req.params.id, req.userId]
    );
    res.json({ success: true, message: 'Notification marked as read' });
  } catch (error) {
    res.status(500).json({ success: false, message: 'Failed to update notification' });
  }
});

// ==================== SEED DATA ====================

async function seedShippingRates() {
  const rates = [
    ['US', 'United States', '美国', 85, 25, 120, 70, '3-7', '20-30', '2-3', '5-10'],
    ['UK', 'United Kingdom', '英国', 75, 22, 110, 65, '3-7', '20-30', '2-3', '5-10'],
    ['DE', 'Germany', '德国', 70, 20, 100, 60, '4-8', '25-35', '2-3', '5-10'],
    ['JP', 'Japan', '日本', 45, 15, 80, 40, '2-4', '10-15', '1-2', '3-5'],
    ['KR', 'South Korea', '韩国', 40, 12, 70, 35, '2-4', '10-15', '1-2', '3-5'],
    ['AU', 'Australia', '澳大利亚', 80, 25, 115, 70, '5-10', '25-35', '3-4', '7-12'],
    ['CA', 'Canada', '加拿大', 82, 24, 118, 68, '5-10', '25-35', '3-4', '7-12'],
    ['SG', 'Singapore', '新加坡', 35, 10, 60, 30, '2-4', '8-12', '1-2', '3-5'],
    ['MY', 'Malaysia', '马来西亚', 38, 12, 65, 32, '3-5', '10-15', '2-3', '4-6'],
    ['TH', 'Thailand', '泰国', 42, 14, 70, 35, '3-5', '10-15', '2-3', '4-6'],
    ['VN', 'Vietnam', '越南', 40, 13, 65, 33, '3-5', '10-15', '2-3', '4-6'],
    ['NZ', 'New Zealand', '新西兰', 85, 28, 120, 75, '7-12', '30-40', '4-5', '10-15'],
    ['TW', 'Taiwan', '台湾', 38, 12, 65, 32, '2-3', '8-12', '1-2', '3-5'],
    ['HK', 'Hong Kong', '香港', 30, 8, 50, 25, '1-2', '5-7', '1', '2-3'],
    ['FR', 'France', '法国', 72, 21, 105, 62, '4-8', '25-35', '2-3', '5-10'],
    ['IT', 'Italy', '意大利', 74, 22, 108, 64, '4-8', '25-35', '2-3', '5-10'],
    ['ES', 'Spain', '西班牙', 76, 23, 110, 66, '4-8', '25-35', '2-3', '5-10'],
    ['RU', 'Russia', '俄罗斯', 68, 18, 95, 55, '7-14', '30-45', '4-6', '10-15'],
    ['BR', 'Brazil', '巴西', 95, 30, 130, 80, '10-15', '35-50', '5-7', '12-18'],
    ['MX', 'Mexico', '墨西哥', 90, 28, 125, 75, '8-12', '30-45', '4-6', '10-15']
  ];

  for (const r of rates) {
    await pool.execute(`
      INSERT INTO shipping_rates 
      (country_code, country_name_en, country_name_zh, air_rate, sea_rate, express_rate, line_rate, air_days, sea_days, express_days, line_days)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      ON DUPLICATE KEY UPDATE
      country_name_en = VALUES(country_name_en),
      country_name_zh = VALUES(country_name_zh),
      air_rate = VALUES(air_rate),
      sea_rate = VALUES(sea_rate),
      express_rate = VALUES(express_rate),
      line_rate = VALUES(line_rate),
      air_days = VALUES(air_days),
      sea_days = VALUES(sea_days),
      express_days = VALUES(express_days),
      line_days = VALUES(line_days)
    `, r);
  }
  console.log('✅ Shipping rates seeded');
}

// ==================== START SERVER ====================
async function start() {
  try {
    await initDatabase();
    await seedShippingRates();
    
    app.listen(PORT, '0.0.0.0', () => {
      console.log(`🚀 CN2Global API running on port ${PORT}`);
      console.log(`📍 http://localhost:${PORT}`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

start();
