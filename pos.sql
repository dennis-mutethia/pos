-- Table structure for table shop_types
CREATE TABLE IF NOT EXISTS shop_types (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  description TEXT,
  created_at TEXT NOT NULL,
  created_by INTEGER NOT NULL,
  updated_at TEXT,
  updated_by INTEGER
);

-- Dumping data for table shop_types
INSERT OR IGNORE INTO shop_types (name, description, created_at, created_by) VALUES
('WINES & SPIRITS / BAR', NULL, DATETIME('now'), 0),
('PHARMACY / CHEMIST', NULL, DATETIME('now'), 0),
('AGROVET', NULL, DATETIME('now'), 0),
('HARDWARE', NULL, DATETIME('now'), 0),
('BUTCHERY', NULL, DATETIME('now'), 0),
('GENERAL SHOP', NULL, DATETIME('now'), 0),
('AUTO SPARE PARTS', NULL, DATETIME('now'), 0),
('BOUTIQUE', NULL, DATETIME('now'), 0),
('CAR DEALER', NULL, DATETIME('now'), 0),
('COSMETIC & BEAUTY', NULL, DATETIME('now'), 0),
('PETROL STATION', NULL, DATETIME('now'), 0),
('GREEN GROCERY', NULL, DATETIME('now'), 0);

-- Table structure for table packages
CREATE TABLE IF NOT EXISTS packages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  amount REAL NULL,
  description TEXT,
  color TEXT,
  validity INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  created_by INTEGER NOT NULL,
  updated_at TEXT,
  updated_by INTEGER
);

-- Dumping data for table packages
INSERT OR IGNORE INTO packages (name, amount, description, color, validity, created_at, created_by) VALUES
('7-DAY TRIAL', 0, 'FREE TRIAL PERIOD', 'danger', 7, DATETIME('now'), 0),
('1-MONTH', 1000, '1 MONTH BASIC PREMIUM PACKAGE', 'success', 31, DATETIME('now'), 0),
('3-MONTHS', 3000, '3 MONTHS BRONZE PACKAGE','warning', 93, DATETIME('now'), 0),
('6-MONTHS S.T.S', 6000,'6 MONTHS SHORT TERM SUPPORT', 'primary', 186, DATETIME('now'), 0),
('1-YEAR L.T.S', 12000, '1 YEAR LONG TERM SUPPORT', 'secondary', 366, DATETIME('now'), 0),
('2-YEARS L.T.S', 24000, '2 YEARS LONG TERM SUPPORT', 'info', 732, DATETIME('now'), 0),
('3-YEARS L.T.S', 36000, '3 YEARS LONG TERM SUPPORT', 'success', 1098, DATETIME('now'), 0);

-- Table structure for table payment_modes
CREATE TABLE IF NOT EXISTS payment_modes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  account TEXT,
  created_at TEXT NOT NULL,
  created_by INTEGER NOT NULL,
  updated_at TEXT,
  updated_by INTEGER
);

-- Dumping data for table payment_modes
INSERT OR IGNORE INTO payment_modes (name, account, created_at, created_by) VALUES
('CASH', NULL,  DATETIME('now'), 0),
('MPESA', NULL,  DATETIME('now'), 0),
('BANK', NULL,  DATETIME('now'), 0),
('N/A', NULL,  DATETIME('now'), 0);

-- Table structure for table payments
CREATE TABLE IF NOT EXISTS payments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  bill_id INTEGER NOT NULL,
  amount REAL NOT NULL,
  payment_mode_id INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  created_by INTEGER NOT NULL,
  updated_at TEXT,
  updated_by INTEGER,
  FOREIGN KEY (payment_mode_id) REFERENCES payment_modes(id)
);

-- Table structure for table licenses
CREATE TABLE IF NOT EXISTS licenses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  key TEXT UNIQUE NOT NULL,
  package_id INTEGER NOT NULL,
  payment_id INTEGER NOT NULL,
  expires_at TEXT NOT NULL,
  created_at TEXT NOT NULL,
  created_by INTEGER NOT NULL,
  updated_at TEXT,
  updated_by INTEGER,
  FOREIGN KEY (package_id) REFERENCES packages(id),
  FOREIGN KEY (payment_id) REFERENCES payments(id)
);

-- Table structure for table companies
CREATE TABLE IF NOT EXISTS companies (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  license_id INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  created_by INTEGER NOT NULL,
  updated_at TEXT,
  updated_by INTEGER,
  FOREIGN KEY (license_id) REFERENCES licenses(id)
);

-- Table structure for table shops
CREATE TABLE IF NOT EXISTS shops (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  shop_type_id INTEGER NOT NULL,
  company_id INTEGER NOT NULL,
  location TEXT NOT NULL,
  phone_1 TEXT,
  phone_2 TEXT,
  paybill TEXT,
  account_no TEXT,
  till_no TEXT,
  created_at TEXT NOT NULL,
  created_by INTEGER NOT NULL,
  updated_at TEXT,
  updated_by INTEGER,
  FOREIGN KEY (shop_type_id) REFERENCES shop_types(id),
  FOREIGN KEY (company_id) REFERENCES companies(id)
);

-- Table structure for table user_levels
CREATE TABLE IF NOT EXISTS user_levels (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  level INTEGER UNIQUE NOT NULL,
  description TEXT,
  created_at TEXT NOT NULL,
  created_by INTEGER NOT NULL,
  updated_at TEXT,
  updated_by INTEGER
);

-- Dumping data for table user_levels
INSERT OR IGNORE INTO user_levels (id, name, level, description, created_at, created_by) VALUES
(0, 'SUPER ADMIN', 0, 'Super User', DATETIME('now'), 0),
(1, 'ADMIN', 1, 'All Permissions<br />\nCan Navigate Multiple Shops', DATETIME('now'), 0),
(2, 'SUPERVISOR', 2, 'Stock<br /> \nInventory<br />\nCustomer Bills<br />\nExpenses<br />\nCan Navigate Multiple Shops', DATETIME('now'), 0),
(3, 'SALES', 3, 'Stock<br /> \nInventory<br /> \nCustomer Bills<br />\nExpenses<br />\nCannot Navigate Multiple Shops', DATETIME('now'), 0),
(4, 'DIRECTOR', 4, 'View Reports Only<br /> \nCan Navigate Multiple Shops', DATETIME('now'), 0);

-- Table structure for table users
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  phone TEXT UNIQUE NOT NULL,
  user_level_id INTEGER NOT NULL,
  shop_id INTEGER NOT NULL,
  password TEXT NOT NULL,
  created_at TEXT NOT NULL,
  created_by INTEGER NOT NULL,
  updated_at TEXT,
  updated_by INTEGER,
  FOREIGN KEY (shop_id) REFERENCES shops(id),
  FOREIGN KEY (user_level_id) REFERENCES user_levels(id)
);
