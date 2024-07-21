-- Table structure for table bills
CREATE TABLE IF NOT EXISTS bills (
  id SERIAL PRIMARY KEY,
  customer_id INT,
  total DOUBLE PRECISION,
  paid DOUBLE PRECISION,
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT,
  PRIMARY KEY (id)
);

-- Table structure for table bill_entries
CREATE TABLE IF NOT EXISTS bill_entries (
  id SERIAL PRIMARY KEY,
  bill_id INT,
  stock_id INT,
  item_name varchar(32),
  price DOUBLE PRECISION,
  qty DOUBLE PRECISION,
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT,
  UNIQUE (bill_id,stock_id,created_by)
);

-- Table structure for table cashbox
CREATE TABLE IF NOT EXISTS cashbox (
  id SERIAL PRIMARY KEY,
  date date,
  amount DOUBLE PRECISION,
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT,
  UNIQUE (date)
);

-- Table structure for table companies
CREATE TABLE IF NOT EXISTS companies (
  id SERIAL PRIMARY KEY,
  name varchar(32),
  license_id INT,
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT,
  UNIQUE (name)
);

-- Table structure for table customers
CREATE TABLE IF NOT EXISTS customers (
  id SERIAL PRIMARY KEY,
  name varchar(32),
  phone varchar(20),
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT,
  UNIQUE (phone)
);

-- Table structure for table debts
CREATE TABLE IF NOT EXISTS debts (
  id SERIAL PRIMARY KEY,
  date date,
  customer_id INT,
  amount DOUBLE PRECISION,
  paid DOUBLE PRECISION DEFAULT '0',
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT
);

-- Table structure for table expenses
CREATE TABLE IF NOT EXISTS expenses (
  id SERIAL PRIMARY KEY,
  date date,
  name varchar(32),
  amount DOUBLE PRECISION,
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT
);

-- Table structure for table licenses
CREATE TABLE IF NOT EXISTS licenses (
  id SERIAL PRIMARY KEY,
  key varchar(512),
  package_id INT,
  expires_at TIMESTAMP,
  payment_id INT,
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT,
  UNIQUE (key)
);

-- Table structure for table license_payments
CREATE TABLE IF NOT EXISTS license_payments (
  id SERIAL PRIMARY KEY,
  ref varchar(32),
  phone varchar(16),
  name varchar(64),
  status INT DEFAULT '0',
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT
);

-- Table structure for table packages
CREATE TABLE IF NOT EXISTS packages (
  id SERIAL PRIMARY KEY,
  name varchar(64),
  amount DOUBLE PRECISION,
  pay DOUBLE PRECISION,
  description varchar(256),
  offer varchar(64),
  color varchar(32),
  validity INT,
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT,
  UNIQUE (name)
);

-- Dumping data for table packages
INSERT INTO packages (id, name, amount, pay, description, offer, color, validity, created_at, created_by, updated_at, updated_by) VALUES
(1, '7-DAY TRIAL', 0, 0, 'FREE TRIAL PERIOD', '', 'danger', 7, '2022-09-29 09:40:32', 1, '2022-10-01 03:48:01', NULL),
(2, '1-MONTH', 1000, 1000, '1 MONTH BASIC PREMIUM PACKAGE', 'STARTER', 'success', 31, '2022-09-29 09:40:32', 1, '2022-12-07 09:55:54', NULL),
(3, '3-MONTHS', 3000, 3000, '3 MONTHS BRONZE PACKAGE', 'OPTIMIZED', 'warning', 93, '2022-09-29 09:40:32', 1, '2022-12-07 09:55:54', NULL),
(4, '6-MONTHS S.T.S', 6000, 5000, '6 MONTHS SHORT TERM SUPPORT', 'SAVE UPTO 10%', 'primary', 186, '2022-09-29 09:40:32', 1, '2022-12-07 09:55:54', NULL),
(5, '1-YEAR L.T.S', 12000, 9000, '1 YEAR LONG TERM SUPPORT', 'SAVE UPTO 15%', 'secondary', 366, '2022-09-29 09:40:32', 1, '2022-12-07 09:55:54', NULL),
(6, '2-YEARS L.T.S', 24000, 16000, '2 YEARS LONG TERM SUPPORT', 'SAVE UPTO 20%', 'info', 732, '2022-09-29 09:40:32', 1, '2022-12-07 09:55:54', NULL),
(7, '3-YEARS L.T.S', 36000, 25000, '3 YEARS LONG TERM SUPPORT', 'SAVE UPTO 30%', 'success', 1098, '2022-10-31 09:53:26', 1, '2022-12-07 09:55:54', NULL);

-- Table structure for table payments
CREATE TABLE IF NOT EXISTS payments (
  id SERIAL PRIMARY KEY,
  bill_id INT,
  amount DOUBLE PRECISION,
  payment_mode_id INT,
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT
);

-- Table structure for table payment_modes
CREATE TABLE IF NOT EXISTS payment_modes (
  id SERIAL PRIMARY KEY,
  name varchar(32),
  account varchar(32),
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT
);

-- Dumping data for table payment_modes

INSERT INTO payment_modes (id, name, account, created_at, created_by, updated_at, updated_by) VALUES
(1, 'CASH', NULL, '2022-12-07 16:36:07', 0, '2022-12-07 13:36:07', NULL),
(2, 'MPESA', NULL, '2022-12-07 16:36:07', 0, '2022-12-07 13:36:07', NULL),
(3, 'BANK', NULL, '2022-12-07 16:36:07', 0, '2022-12-07 13:36:07', NULL),
(4, 'N/A', NULL, '2022-12-07 16:36:07', 0, '2022-12-07 13:36:07', NULL);

-- Table structure for table shop_types
CREATE TABLE IF NOT EXISTS shop_types (
  id SERIAL PRIMARY KEY,
  name varchar(32),
  description varchar(1028),
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT
);

-- Dumping data for table shop_types
INSERT INTO shop_types (id, name, description, created_at, created_by, updated_at, updated_by) VALUES
(1, 'WINES & SPIRITS / BAR', NULL, NULL, 0, '2023-01-02 16:16:01', NULL),
(2, 'PHARMACY / CHEMIST', NULL, NULL, 0, '2023-01-02 16:16:07', NULL),
(3, 'AGROVET', NULL, NULL, 0, '2022-12-30 07:44:46', NULL),
(4, 'HARDWARE', NULL, NULL, 0, '2022-12-30 07:44:46', NULL),
(5, 'BUTCHERY', NULL, NULL, 0, '2022-12-30 07:44:46', NULL),
(6, 'GENERAL SHOP', NULL, NULL, 0, '2023-01-02 16:16:17', NULL),
(7, 'AUTO SPARE PARTS', NULL, NULL, 0, '2022-12-30 07:44:28', NULL),
(8, 'BOUTIQUE', NULL, '2023-01-02 19:13:35', 0, '2023-01-02 16:13:35', NULL),
(9, 'CAR DEALER', NULL, '2023-01-02 19:13:35', 0, '2023-01-02 16:13:35', NULL),
(10, 'COSMETIC & BEAUTY', NULL, '2023-01-02 19:14:46', 0, '2023-01-02 16:14:46', NULL),
(11, 'PETROL STATION', NULL, '2023-01-02 19:14:46', 0, '2023-01-02 16:14:46', NULL),
(12, 'GREEN GROCERY', NULL, '2023-01-02 19:14:46', 0, '2023-01-02 16:14:46', NULL);

-- Table structure for table product_categories
CREATE TABLE IF NOT EXISTS product_categories (
  id SERIAL PRIMARY KEY,
  name varchar(32),
  shop_type_id INT,
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT,
  UNIQUE (name)
);

--
-- Dumping data for table product_categories
--

INSERT INTO product_categories (id, name, created_at, created_by, updated_at, updated_by) VALUES
(1, 'BOTTLES', '2022-10-02 11:57:49', 26, '2022-10-02 05:57:49', NULL),
(2, 'CANS', '2022-10-02 11:57:58', 26, '2022-10-02 05:57:58', NULL),
(3, 'SOFT DRINKS', '2022-10-02 11:58:08', 26, '2022-10-02 05:58:08', NULL),
(4, 'QUARTERS - 250ML', '2022-10-02 11:58:55', 26, '2022-10-02 05:59:17', 26),
(5, 'NUSU - 350ML', '2022-10-02 11:59:08', 26, '2022-10-02 05:59:08', NULL),
(6, 'MIZINGA', '2022-10-02 11:59:41', 26, '2022-10-02 05:59:41', NULL),
(7, 'WINES', '2022-10-02 12:32:07', 26, '2022-10-02 06:32:07', NULL),
(8, 'CIGARETTES', '2022-10-02 12:36:07', 26, '2022-10-02 06:36:07', NULL),
(9, 'TOTS', '2022-10-02 13:02:24', 26, '2022-10-02 07:02:24', NULL),
(10, 'OTHERS', '2022-10-02 14:50:45', 26, '2022-10-02 08:50:45', NULL);
UPDATE product_categories SET shop_type_id=1 WHERE id>0;

-- Table structure for table products
CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  name varchar(32),
  purchase_price DOUBLE PRECISION,
  selling_price DOUBLE PRECISION,
  category_id INT,
  shop_type_id INT,
  current_stock DOUBLE PRECISION DEFAULT '0',
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT,
  UNIQUE (name, category_id)
);

-- Dumping data for table products
INSERT INTO products (id, name, purchase_price, selling_price, category_id, current_stock, created_at, created_by, updated_at, updated_by) VALUES
(14, 'WATER 500ML', 70, 100, 3, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(18, 'KC 250ML', 210, 300, 4, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(20, 'PET SODA', 70, 100, 3, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(21, 'TONIC', 35, 50, 3, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(23, 'SODA 500ML', 70, 100, 3, 0, '2022-09-26 00:00:00', 1, '2022-10-02 08:11:40', 26),
(25, 'KIBAO 250ML', 175, 250, 4, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(26, 'KC 350ML', 385, 550, 5, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(28, 'PREDATOR ENERGY', 42, 60, 3, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(32, 'TUSKER LITE CAN', 154, 220, 2, 0, '2022-09-26 00:00:00', 1, '2022-10-02 08:11:40', 26),
(33, 'QUE WATER 1/2', 35, 50, 3, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(36, 'VICEROY 350ML', 630, 900, 5, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(37, 'RICHOT 350ML', 630, 900, 5, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(38, 'GILBEYS 350ML', 630, 900, 5, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(40, 'TUSKER CIDAR CAN', 175, 250, 2, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(46, 'WHITECAP CAN', 175, 250, 2, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(49, 'BLACK ICE CAN', 175, 250, 2, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(53, 'GUINESS CAN', 175, 250, 2, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(58, '4 COUSINS 750ML', 840, 1200, 7, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(59, 'VAT69 350ML', 700, 1000, 5, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(63, 'ORIGIN 250ML', 175, 250, 4, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(65, 'VICEROY 250ML', 385, 550, 4, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(66, 'FAMOUS GROUSE 350ML', 909.9999999999999, 1300, 5, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(67, 'KINGFISHER', 154, 220, 7, 0, '2022-09-26 00:00:00', 1, '2022-10-02 08:11:40', 26),
(68, 'PENASOL', 489.99999999999994, 700, 7, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(70, 'GUARANA CAN', 175, 250, 2, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(72, 'RED LABEL 350ML', 1050, 1500, 5, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(74, 'FAXE CAN', 175, 250, 2, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(75, 'GRANTS 350ML', 700, 1000, 5, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(76, 'DROSTOFF', 840, 1200, 7, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(77, 'SPORTSMAN', 210, 300, 8, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(78, 'DUNHILL', 280, 400, 8, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(79, 'JAMESON 350ML', 1050, 1700, 5, 0, '2022-09-26 00:00:00', 1, '2022-10-04 09:41:27', 11),
(80, 'BLACK & WHITE 350ML', 489.99999999999994, 700, 5, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(83, 'REDBULL', 140, 200, 2, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(86, 'HEINEKEN CAN', 175, 250, 2, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(91, 'BLACK LABEL 350ML', 1400, 2000, 5, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(93, 'BALOZI CAN', 154, 220, 2, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(95, 'SNAPP CAN', 175, 250, 2, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(97, 'TUSKER MALT CAN', 175, 250, 2, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(98, 'MANGO', 210, 300, 3, 0, '2022-09-26 00:00:00', 1, '2022-10-02 07:10:20', 26),
(99, 'SMIRNOFF VODKA 250ML', 385, 550, 4, 0, '2022-09-27 07:03:24', 12, '2022-10-02 07:10:20', 26),
(100, 'HUNTERS 350ML', 350, 500, 5, 0, '2022-09-27 13:15:28', 12, '2022-10-02 07:10:20', 26),
(101, 'SMIRNOFF VODKA 350ML', 630, 900, 5, 0, '2022-09-27 13:15:50', 12, '2022-10-02 07:10:20', 26),
(102, 'WILLIAM LAWSONS 350ML', 1400, 2000, 5, 0, '2022-09-27 13:16:09', 12, '2022-10-02 07:10:20', 26),
(103, 'CELLAR CASK 750ML', 1050, 1500, 7, 0, '2022-09-27 13:17:13', 12, '2022-10-02 07:10:20', 26),
(104, 'CASSABUENA', 489.99999999999994, 700, 7, 0, '2022-09-27 13:17:41', 12, '2022-10-02 07:10:20', 26),
(105, '4TH STREET 750ML', 1050, 1500, 7, 0, '2022-09-27 13:18:06', 12, '2022-10-02 07:10:20', 26),
(106, 'CAPRICE', 560, 800, 7, 0, '2022-09-27 13:18:20', 12, '2022-10-02 07:10:20', 26),
(107, 'KC 750ML', 630, 900, 6, 0, '2022-09-27 13:18:41', 12, '2022-10-02 07:10:20', 26),
(108, 'CHROME 750ML', 560, 800, 6, 0, '2022-09-27 13:19:00', 12, '2022-10-02 07:10:20', 26),
(109, 'SMIRNOFF VODKA 750ML', 1190, 1700, 6, 0, '2022-09-27 13:19:14', 12, '2022-10-02 07:10:20', 26),
(114, 'SODA 300ML', 35, 50, 3, 0, '2022-09-27 13:23:26', 12, '2022-10-02 07:10:20', 26),
(115, 'WATER 300ML', 35, 50, 3, 0, '2022-09-27 13:23:54', 12, '2022-10-02 07:10:20', 26),
(119, 'GUINESS SMOOTH CAN', 175, 250, 2, 0, '2022-09-27 13:26:50', 12, '2022-10-02 07:10:20', 26),
(120, 'TUSKER CAN', 175, 250, 2, 0, '2022-09-27 14:53:57', 12, '2022-10-02 07:10:20', 26),
(122, 'SMIRNOFF VODKA TOT', 70, 100, 9, 0, '2022-09-27 14:58:18', 12, '2022-10-02 07:10:20', 26),
(123, 'KIBAO 750ML', 560, 800, 6, 0, '2022-09-27 16:17:25', 12, '2022-10-02 07:10:20', 26),
(124, 'TUSKER', 154, 220, 1, 0, '2022-10-02 12:01:47', 26, '2022-10-02 07:10:20', NULL),
(125, 'TUSKER LITE', 175, 220, 1, 0, '2022-10-02 12:02:06', 26, '2022-10-03 10:48:34', 28),
(128, 'SMIRNOFF ICE', 154, 220, 1, 0, '2022-10-02 12:03:03', 26, '2022-10-02 08:11:40', NULL),
(129, 'SNAPP', 161, 230, 1, 0, '2022-10-02 12:03:19', 26, '2022-10-02 07:10:20', NULL),
(130, 'PILSNER', 154, 220, 1, 0, '2022-10-02 12:03:32', 26, '2022-10-02 07:10:20', NULL),
(131, 'GUINESS', 161, 230, 1, 0, '2022-10-02 12:03:49', 26, '2022-10-02 07:10:20', NULL),
(132, 'BALOZI', 154, 220, 1, 0, '2022-10-02 12:04:04', 26, '2022-10-02 07:10:20', NULL),
(133, 'WHITECAP', 154, 220, 1, 0, '2022-10-02 12:04:16', 26, '2022-10-02 07:10:20', NULL),
(135, 'GUINESS SMOOTH', 154, 220, 1, 0, '2022-10-02 12:04:51', 26, '2022-10-02 07:10:20', NULL),
(136, 'SUMMIT', 140, 200, 1, 0, '2022-10-02 12:05:07', 26, '2022-10-02 07:10:20', NULL),
(137, 'HUNTERS CIDAR', 140, 200, 1, 0, '2022-10-02 12:05:34', 26, '2022-10-02 07:10:20', NULL),
(138, 'SAVANNAH CIDAR', 175, 250, 1, 0, '2022-10-02 12:06:02', 26, '2022-10-02 07:10:20', NULL),
(139, 'HEINEKEN', 175, 250, 1, 0, '2022-10-02 12:06:23', 26, '2022-10-02 07:10:20', NULL),
(140, 'MONSTER CAN', 175, 250, 2, 0, '2022-10-02 12:10:25', 26, '2022-10-02 07:10:20', NULL),
(141, 'SMIRNOFF VODKA 1L', 1400, 2000, 6, 0, '2022-10-02 12:18:08', 26, '2022-10-02 07:10:20', 26),
(142, 'VICEROY 750ML', 1260, 1800, 6, 0, '2022-10-02 12:18:54', 26, '2022-10-02 07:10:20', NULL),
(143, 'RICHOT 750ML', 1190, 1700, 6, 0, '2022-10-02 12:19:09', 26, '2022-10-02 07:10:20', NULL),
(144, 'HUNTERS 750ML', 770, 1100, 6, 0, '2022-10-02 12:19:24', 26, '2022-10-02 07:10:20', NULL),
(145, 'FRONTELA 750ML', 1050, 1500, 6, 0, '2022-10-02 12:19:45', 26, '2022-10-02 07:10:20', NULL),
(146, 'CARLO ROSSI 750ML', 1050, 1500, 6, 0, '2022-10-02 12:20:13', 26, '2022-10-02 07:10:20', NULL),
(147, 'ALL SEASONS 750ML', 1050, 1500, 6, 0, '2022-10-02 12:20:32', 26, '2022-10-02 07:10:20', NULL),
(148, 'GILBEYS GIN 750ML', 1190, 1700, 6, 0, '2022-10-02 12:20:50', 26, '2022-10-02 07:10:20', NULL),
(149, 'VAT69 750ML', 1400, 2000, 6, 0, '2022-10-02 12:21:20', 26, '2022-10-02 07:10:20', NULL),
(150, 'V&A 750ML', 700, 1000, 6, 0, '2022-10-02 12:21:59', 26, '2022-10-02 06:21:59', NULL),
(151, 'HIGHLAND QUEEN 1L', 1260, 1800, 6, 0, '2022-10-02 12:22:23', 26, '2022-10-02 07:10:20', NULL),
(152, 'FAMOUSE GROUSE 750ML', 1750, 2500, 6, 0, '2022-10-02 12:22:49', 26, '2022-10-02 07:10:20', NULL),
(153, 'RED LABEL 750ML', 1750, 2500, 6, 0, '2022-10-02 12:23:50', 26, '2022-10-02 07:10:20', NULL),
(154, 'GRANT 750ML', 1400, 2000, 6, 0, '2022-10-02 12:24:05', 26, '2022-10-02 08:11:40', NULL),
(155, 'JAMESON 750ML', 1959.9999999999998, 2800, 6, 0, '2022-10-02 12:24:22', 26, '2022-10-02 07:10:20', NULL),
(156, 'BLACK & WHITE 750ML', 1050, 1500, 6, 0, '2022-10-02 12:24:52', 26, '2022-10-02 07:10:20', NULL),
(157, 'WILLIAM LAWSONS 750ML', 1050, 1500, 6, 0, '2022-10-02 12:25:09', 26, '2022-10-02 07:10:20', NULL),
(158, 'BEST WHISKEY 750ML', 840, 1200, 6, 0, '2022-10-02 12:26:05', 26, '2022-10-02 07:10:20', NULL),
(159, 'BLACK LABEL 750ML', 2660, 3800, 6, 0, '2022-10-02 12:26:28', 26, '2022-10-02 07:10:20', NULL),
(160, 'JACK DANIELS 750ML', 2800, 4000, 6, 0, '2022-10-02 12:26:49', 26, '2022-10-02 07:10:20', NULL),
(161, 'BEST GIN 750ML', 700, 1000, 6, 0, '2022-10-02 12:27:11', 26, '2022-10-02 06:27:11', NULL),
(162, 'BEST CREAM 750ML', 1050, 1500, 6, 0, '2022-10-02 12:27:29', 26, '2022-10-02 07:10:20', NULL),
(163, 'GENERAL MEAKENS 750ML', 560, 800, 6, 0, '2022-10-02 12:27:53', 26, '2022-10-02 07:10:20', NULL),
(164, 'KK 750ML', 420, 600, 6, 0, '2022-10-02 12:28:12', 26, '2022-10-02 07:10:20', NULL),
(165, 'NAPS 750ML', 560, 800, 6, 0, '2022-10-02 12:28:28', 26, '2022-10-02 07:10:20', NULL),
(166, 'WHITE PEARL 750ML', 420, 600, 6, 0, '2022-10-02 12:28:44', 26, '2022-10-02 07:10:20', NULL),
(167, 'CHIVAS 750ML', 3500, 5000, 6, 0, '2022-10-02 12:29:09', 26, '2022-10-02 06:29:09', NULL),
(168, 'SOUTHERN COMFORT 750ML', 1750, 2500, 6, 0, '2022-10-02 12:29:53', 26, '2022-10-02 07:10:20', NULL),
(169, 'BAILEYS ORIGINAL 750ML', 2100, 3000, 6, 0, '2022-10-02 12:30:14', 26, '2022-10-02 07:10:20', NULL),
(170, 'AMARULA 750ML', 1750, 2500, 6, 0, '2022-10-02 12:30:33', 26, '2022-10-02 07:10:20', NULL),
(171, 'AMARULA 1L', 2450, 3500, 6, 0, '2022-10-02 12:30:48', 26, '2022-10-02 07:10:20', NULL),
(172, 'MALIBU 750ML', 1050, 1500, 6, 0, '2022-10-02 12:31:04', 26, '2022-10-02 07:10:20', NULL),
(173, 'BAILEYS DELIGHT 750ML', 1050, 1500, 6, 0, '2022-10-02 12:31:27', 26, '2022-10-02 07:10:20', NULL),
(174, 'CAPTAIN MORGAN 750ML', 770, 1100, 6, 0, '2022-10-02 12:31:45', 26, '2022-10-02 08:11:40', NULL),
(175, 'EMBASSY', 280, 400, 8, 0, '2022-10-02 12:36:48', 26, '2022-10-02 07:10:20', NULL),
(176, 'SAFARI', 175, 250, 8, 0, '2022-10-02 12:37:03', 26, '2022-10-02 07:10:20', NULL),
(177, 'RICHOT 250ML', 385, 550, 4, 0, '2022-10-02 12:39:09', 26, '2022-10-02 07:10:20', NULL),
(178, 'HUNTERS 250ML', 244.99999999999997, 350, 4, 0, '2022-10-02 12:39:27', 26, '2022-10-02 07:10:20', NULL),
(179, 'GILBEYS 250ML', 385, 550, 4, 0, '2022-10-02 12:39:42', 26, '2022-10-02 07:10:20', NULL),
(180, 'V&A 250ML', 210, 300, 4, 0, '2022-10-02 12:39:55', 26, '2022-10-02 07:10:20', NULL),
(181, 'RED LABEL 250ML', 489.99999999999994, 700, 4, 0, '2022-10-02 12:40:30', 26, '2022-10-02 08:11:40', 26),
(182, 'BEST CREAM 250ML', 315, 450, 4, 0, '2022-10-02 12:41:07', 26, '2022-10-02 07:10:20', 26),
(183, 'BEST WHISKY 250ML', 280, 400, 4, 0, '2022-10-02 12:41:26', 26, '2022-10-02 07:10:20', NULL),
(184, 'BLACK LABEL 250ML', 944.9999999999999, 1350, 4, 0, '2022-10-02 12:41:44', 26, '2022-10-02 07:10:20', NULL),
(185, 'BEST GIN 250ML', 385, 550, 4, 0, '2022-10-02 12:42:08', 26, '2022-10-02 07:10:20', NULL),
(186, 'BOND 7 250ML', 350, 500, 4, 0, '2022-10-02 12:42:25', 26, '2022-10-02 07:10:20', NULL),
(187, 'GENERAL MEAKEANS 250ML', 175, 250, 4, 0, '2022-10-02 12:42:47', 26, '2022-10-02 07:10:20', NULL),
(188, 'KK 250ML', 154, 220, 4, 0, '2022-10-02 12:43:03', 26, '2022-10-02 07:10:20', NULL),
(189, 'NAPS 250ML', 175, 250, 4, 0, '2022-10-02 12:43:17', 26, '2022-10-02 07:10:20', NULL),
(190, 'WHITEPEARL 250ML', 154, 220, 4, 0, '2022-10-02 12:43:33', 26, '2022-10-02 07:10:20', NULL),
(191, 'CAPTAIN MORGAN 250ML', 244.99999999999997, 350, 4, 0, '2022-10-02 12:44:13', 26, '2022-10-02 07:10:20', NULL),
(192, 'BEST GIN 350ML', 385, 550, 5, 0, '2022-10-02 12:53:23', 26, '2022-10-02 07:10:20', NULL),
(194, 'BAILEYS ORIGINAL 350ML', 1050, 1500, 5, 0, '2022-10-02 12:54:58', 26, '2022-10-02 07:10:20', NULL),
(195, 'JACK DANIELS 350ML', 1400, 2000, 5, 0, '2022-10-02 12:58:57', 26, '2022-10-02 07:10:20', NULL),
(196, 'BEST CREAM 350ML', 350, 500, 5, 0, '2022-10-02 12:59:26', 26, '2022-10-02 07:10:20', NULL),
(197, 'BOND 7 350ML', 489.99999999999994, 700, 5, 0, '2022-10-02 13:00:12', 26, '2022-10-02 07:10:20', NULL),
(198, 'GILBEYS TOOT', 70, 100, 9, 0, '2022-10-02 13:03:15', 26, '2022-10-02 07:10:20', NULL),
(199, 'VAT69 TOT', 105, 150, 9, 0, '2022-10-02 13:03:29', 26, '2022-10-02 07:10:20', NULL),
(200, 'FAMOUS GROUSE TOT', 105, 150, 9, 0, '2022-10-02 13:03:48', 26, '2022-10-02 07:10:20', NULL),
(201, 'BLACK LABEL TOT', 140, 200, 9, 0, '2022-10-02 13:04:07', 26, '2022-10-02 07:10:20', NULL),
(202, 'LIME JUICE TOT', 14, 20, 9, 0, '2022-10-02 13:04:22', 26, '2022-10-02 07:10:20', NULL),
(203, 'TUSKER MALT', 154, 220, 1, 0, '2022-10-02 13:05:18', 26, '2022-10-02 08:11:40', NULL),
(204, 'TUSKER CIDAR', 154, 220, 1, 0, '2022-10-02 13:05:31', 26, '2022-10-02 08:11:40', NULL),
(205, 'WHITECAP LITE', 154, 220, 1, 0, '2022-10-02 13:06:26', 26, '2022-10-02 07:10:20', NULL),
(206, 'COUNTY 250ML', 175, 250, 4, 0, '2022-10-02 14:09:14', 26, '2022-10-02 08:11:40', NULL),
(207, 'BLACK & WHITE 250ML', 385, 550, 4, 0, '2022-10-02 14:10:31', 26, '2022-10-02 08:11:40', NULL),
(208, 'CHROME 250ML', 175, 250, 4, 0, '2022-10-02 14:29:41', 26, '2022-10-02 08:29:41', NULL),
(209, 'TRUST', 70, 100, 10, 0, '2022-10-02 14:51:11', 26, '2022-10-02 08:51:11', NULL);
UPDATE products SET shop_type_id=1 WHERE id>0;

-- Table structure for table shops
CREATE TABLE IF NOT EXISTS shops (
  id SERIAL PRIMARY KEY,
  name varchar(32),
  location varchar(32),
  company_id INT,
  shop_type_id INT,
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT,
  phone_1 varchar(20),
  phone_2 varchar(20),
  paybill varchar(16),
  account_no varchar(32),
  till_no varchar(16),
  UNIQUE (name)
);

-- Table structure for table stock
CREATE TABLE IF NOT EXISTS stock (
  id SERIAL PRIMARY KEY,
  product_id INT,
  date date,
  name varchar(32),
  category_id INT,
  purchase_price DOUBLE PRECISION,
  selling_price DOUBLE PRECISION,
  opening DOUBLE PRECISION,
  additions DOUBLE PRECISION,
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT,
  UNIQUE (date,name,category_id)
);

-- Table structure for table users
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name varchar(64),
  phone varchar(20),
  shop_id INT,
  user_level INT DEFAULT '0',
  pwd varchar(256),
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT,
  UNIQUE (phone)
);

-- Table structure for table user_levels
CREATE TABLE IF NOT EXISTS user_levels (
  id SERIAL PRIMARY KEY,
  name varchar(32),
  level INT DEFAULT '0',
  description varchar(1028),
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT,
  UNIQUE (level)
);

-- Dumping data for table user_levels
INSERT INTO user_levels (id, name, level, description, created_at, created_by, updated_at, updated_by) VALUES
(0, 'SUPER ADMIN', 0, 'All Permissions<br />Can access admin portal', NOW(),0, NULL, NULL),
(1, 'ADMIN', 1, 'All Permissions<br />\nCan Navigate Multiple Shops', NOW(), 0, NULL, NULL),
(2, 'SUPERVISOR', 2, 'Stock<br /> \nInventory<br />\nCustomer Bills<br />\nExpenses<br />\nCan Navigate Multiple Shops', NOW(), 0,NULL, NULL),
(3, 'SALES', 3, 'Stock<br /> \nInventory<br /> \nCustomer Bills<br />\nExpenses<br />\nCannot Navigate Multiple Shops', NOW(), 0, NULL, NULL),
(4, 'DIRECTOR', 4, 'View Reports Only<br /> \nCan Navigate Multiple Shops', NOW(), 0, NULL, NULL);

CREATE TABLE change_log (
  id SERIAL PRIMARY KEY,
  date date,
  version varchar(16),
  menu varchar(16),
  submenu varchar(32),
  description varchar(1028),
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP,
  updated_by INT
);
