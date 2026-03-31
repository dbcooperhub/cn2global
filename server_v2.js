const express = require('express');
const mysql = require('mysql2/promise');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const { body, validationResult } = require('express-validator');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'cn2global-secret-key-2024';

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

// Register with phone and country code
app.post('/api/auth/register',
  [
    body('phone').optional().isLength({ min: 4, max: 15 }),
    body('email').optional().isEmail(),
    body('password').optional().isLength({ min: 6 }),
    body('country_code').optional().isLength({ min: 1, max: 5 })
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ success: false, errors: errors.array() });
      }

      const { phone, email, password, name, country_code, google_id, google_token } = req.body;
      
      // Google OAuth registration
      if (google_id || google_token) {
        // Verify Google token (simplified - in production use google-auth-library)
        const googleEmail = email;
        const googleName = name;
        
        // Check if user exists
        const [existingUsers] = await pool.execute(
          'SELECT * FROM users WHERE email = ? OR google_id = ?',
          [googleEmail, google_id]
        );
        
        if (existingUsers.length > 0) {
          // Login existing user
          const user = existingUsers[0];
          const token = jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '7d' });
          return res.json({
            success: true,
            message: 'Login successful',
            data: {
              userId: user.id,
              token,
              name: user.name,
              email: user.email,
              memberLevel: user.member_level,
              isNewUser: false
            }
          });
        }
        
        // Create new Google user
        const [result] = await pool.execute(
          'INSERT INTO users (email, name, google_id, member_level) VALUES (?, ?, ?, "normal")',
          [googleEmail, googleName, google_id]
        );
        
        const token = jwt.sign({ userId: result.insertId }, JWT_SECRET, { expiresIn: '7d' });
        
        return res.json({
          success: true,
          message: 'Registration successful',
          data: {
            userId: result.insertId,
            token,
            name: googleName,
            email: googleEmail,
            memberLevel: 'normal',
            isNewUser: true
          }
        });
      }
      
      // Regular registration
      if (!phone && !email) {
        return res.status(400).json({ success: false, message: 'Phone or email required' });
      }
      
      if (!password) {
        return res.status(400).json({ success: false, message: 'Password required' });
      }

      const hashedPassword = await bcrypt.hash(password, 10);
      const fullPhone = country_code && phone ? `${country_code}${phone}` : phone;

      const [result] = await pool.execute(
        'INSERT INTO users (phone, email, password, name, country_code) VALUES (?, ?, ?, ?, ?)',
        [fullPhone || null, email || null, hashedPassword, name || null, country_code || null]
      );

      const token = jwt.sign({ userId: result.insertId }, JWT_SECRET, { expiresIn: '7d' });
      const warehouseCode = 'CN2G' + result.insertId.toString().padStart(6, '0');

      res.json({
        success: true,
        message: 'Registration successful',
        data: {
          userId: result.insertId,
          token,
          warehouseCode,
          isNewUser: true
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
    const { account, password } = req.body;

    const [users] = await pool.execute(
      'SELECT * FROM users WHERE phone = ? OR email = ?',
      [account, account]
    );

    if (users.length === 0) {
      return res.status(401).json({ success: false, message: 'Account not found' });
    }

    const user = users[0];
    
    // Check if Google account without password
    if (!user.password && user.google_id) {
      return res.status(400).json({ success: false, message: 'Please login with Google' });
    }
    
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
        email: user.email,
        phone: user.phone,
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

// Google Login
app.post('/api/auth/google', async (req, res) => {
  try {
    const { google_id, email, name, google_token } = req.body;
    
    if (!email) {
      return res.status(400).json({ success: false, message: 'Email required from Google' });
    }

    // Check if user exists
    const [users] = await pool.execute(
      'SELECT * FROM users WHERE email = ?',
      [email]
    );

    if (users.length > 0) {
      // Update Google ID if not set
      const user = users[0];
      if (!user.google_id) {
        await pool.execute('UPDATE users SET google_id = ? WHERE id = ?', [google_id, user.id]);
      }
      
      const token = jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '7d' });
      return res.json({
        success: true,
        message: 'Login successful',
        data: {
          userId: user.id,
          token,
          name: user.name,
          email: user.email,
          memberLevel: user.member_level,
          isNewUser: false
        }
      });
    }

    // Create new user
    const [result] = await pool.execute(
      'INSERT INTO users (email, name, google_id, member_level) VALUES (?, ?, ?, "normal")',
      [email, name || 'Google User', google_id]
    );

    const token = jwt.sign({ userId: result.insertId }, JWT_SECRET, { expiresIn: '7d' });

    res.json({
      success: true,
      message: 'Registration successful',
      data: {
        userId: result.insertId,
        token,
        name: name || 'Google User',
        email,
        memberLevel: 'normal',
        isNewUser: true
      }
    });
  } catch (error) {
    console.error('Google auth error:', error);
    res.status(500).json({ success: false, message: 'Google authentication failed' });
  }
});

// Get current user
app.get('/api/auth/me', authMiddleware, async (req, res) => {
  try {
    const [users] = await pool.execute(
      'SELECT id, phone, email, name, country_code, member_level, points, balance, created_at FROM users WHERE id = ?',
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

// Update user phone
app.put('/api/auth/phone', authMiddleware, async (req, res) => {
  try {
    const { phone, country_code } = req.body;
    const fullPhone = country_code && phone ? `${country_code}${phone}` : phone;
    
    await pool.execute(
      'UPDATE users SET phone = ?, country_code = ? WHERE id = ?',
      [fullPhone, country_code, req.userId]
    );
    
    res.json({ success: true, message: 'Phone updated' });
  } catch (error) {
    if (error.code === 'ER_DUP_ENTRY') {
      return res.status(400).json({ success: false, message: 'Phone already in use' });
    }
    res.status(500).json({ success: false, message: 'Failed to update phone' });
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
    res.status(500).json({ success: false, message: 'Failed to get addresses' });
  }
});

// Add address
app.post('/api/addresses', authMiddleware, async (req, res) => {
  try {
    const { country, state, city, street, zip_code, contact_name, contact_phone, is_default } = req.body;

    if (is_default) {
      await pool.execute('UPDATE addresses SET is_default = FALSE WHERE user_id = ?', [req.userId]);
    }

    const [result] = await pool.execute(
      'INSERT INTO addresses (user_id, country, state, city, street, zip_code, contact_name, contact_phone, is_default) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
      [req.userId, country, state, city, street, zip_code, contact_name, contact_phone, is_default || false]
    );

    res.json({ success: true, message: 'Address added', data: { addressId: result.insertId } });
  } catch (error) {
    res.status(500).json({ success: false, message: 'Failed to add address' });
  }
});

// Delete address
app.delete('/api/addresses/:id', authMiddleware, async (req, res) => {
  try {
    await pool.execute('DELETE FROM addresses WHERE id = ? AND user_id = ?', [req.params.id, req.userId]);
    res.json({ success: true, message: 'Address deleted' });
  } catch (error) {
    res.status(500).json({ success: false, message: 'Failed to delete address' });
  }
});

// ==================== WAREHOUSE ====================

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

// ==================== PACKAGES ====================

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
    res.status(500).json({ success: false, message: 'Failed to get packages' });
  }
});

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
    res.status(500).json({ success: false, message: 'Failed to submit forecast' });
  }
});

// ==================== SHIPPING RATES ====================

app.get('/api/rates', async (req, res) => {
  try {
    const [rates] = await pool.execute('SELECT * FROM shipping_rates ORDER BY country_name_en');
    res.json({ success: true, data: rates });
  } catch (error) {
    res.status(500).json({ success: false, message: 'Failed to get rates' });
  }
});

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

    const baseFee = weight * parseFloat(rate[rateField]);
    const handlingFee = 30;
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
    res.status(500).json({ success: false, message: 'Calculation failed' });
  }
});

// ==================== ORDERS ====================

app.post('/api/orders', authMiddleware, async (req, res) => {
  const conn = await pool.getConnection();
  try {
    await conn.beginTransaction();

    const { address_id, package_ids, shipping_method, service_options } = req.body;
    const orderNumber = 'ORD' + Date.now().toString(36).toUpperCase();

    const [packages] = await conn.execute(
      'SELECT SUM(actual_weight) as total_weight FROM packages WHERE id IN (?) AND user_id = ?',
      [package_ids, req.userId]
    );

    const totalWeight = packages[0].total_weight || 0;

    const [addrResult] = await conn.execute('SELECT country FROM addresses WHERE id = ?', [address_id]);
    const countryCode = addrResult[0]?.country;

    const [rates] = await conn.execute('SELECT * FROM shipping_rates WHERE country_code = ?', [countryCode]);
    const rate = rates[0];
    const rateField = shipping_method + '_rate';

    const baseFee = totalWeight * parseFloat(rate[rateField]);
    const handlingFee = 30;
    const serviceFee = service_options?.reduce((sum, opt) => sum + opt.price, 0) || 0;
    const totalFee = baseFee + handlingFee + serviceFee;

    const [orderResult] = await conn.execute(
      'INSERT INTO orders (order_number, user_id, address_id, shipping_method, total_weight, base_fee, service_fee, total_fee, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, "pending_payment")',
      [orderNumber, req.userId, address_id, shipping_method, totalWeight, baseFee, serviceFee, totalFee]
    );

    const orderId = orderResult.insertId;

    const orderItems = package_ids.map(pid => [orderId, pid]);
    await conn.execute('INSERT INTO order_items (order_id, package_id) VALUES ?', [orderItems]);

    await conn.execute(
      'INSERT INTO tracking_history (order_id, status, location, description) VALUES (?, "order_created", "Qingdao, China", "Order created, pending payment")',
      [orderId]
    );

    await conn.commit();

    res.json({
      success: true,
      message: 'Order created',
      data: { orderId, orderNumber, totalFee: totalFee.toFixed(2) }
    });
  } catch (error) {
    await conn.rollback();
    res.status(500).json({ success: false, message: 'Failed to create order' });
  } finally {
    conn.release();
  }
});

app.get('/api/orders', authMiddleware, async (req, res) => {
  try {
    const [orders] = await pool.execute(
      `SELECT o.*, a.country, a.city, a.contact_name 
       FROM orders o 
       LEFT JOIN addresses a ON o.address_id = a.id 
       WHERE o.user_id = ?
       ORDER BY o.created_at DESC`,
      [req.userId]
    );
    res.json({ success: true, data: orders });
  } catch (error) {
    res.status(500).json({ success: false, message: 'Failed to get orders' });
  }
});

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
      data: { order: orders[0], tracking }
    });
  } catch (error) {
    res.status(500).json({ success: false, message: 'Tracking failed' });
  }
});

// ==================== START SERVER ====================
async function start() {
  try {
    // Add google_id column if not exists
    const conn = await pool.getConnection();
    await conn.execute('ALTER TABLE users ADD COLUMN IF NOT EXISTS google_id VARCHAR(100)').catch(() => {});
    await conn.execute('ALTER TABLE users ADD COLUMN IF NOT EXISTS country_code VARCHAR(10)').catch(() => {});
    conn.release();
    
    app.listen(PORT, '0.0.0.0', () => {
      console.log(`CN2Global API running on port ${PORT}`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

start();
