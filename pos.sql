-- Table structure for table `user_levels`
CREATE TABLE IF NOT EXISTS `user_levels` (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  level INTEGER UNIQUE NOT NULL,
  description TEXT,
  created_at TEXT NOT NULL,
  created_by INTEGER NOT NULL,
  updated_at TEXT,
  updated_by INTEGER
);

-- Dumping data for table `user_levels`
INSERT INTO `user_levels` (`id`, `name`, `level`, `description`, `created_at`, `created_by`, `updated_at`, `updated_by`) VALUES
(1, 'ADMIN', 1, 'All Permissions<br />\nCan Navigate Multiple Shops', '2022-09-13 22:44:25', 0, '2022-09-25 13:12:44', NULL),
(2, 'SUPERVISOR', 2, 'Stock<br /> \nInventory<br />\nCustomer Bills<br />\nExpenses<br />\nCan Navigate Multiple Shops', '2022-09-13 22:44:25', 0, '2022-09-25 13:14:13', NULL),
(3, 'SALES', 3, 'Stock<br /> \nInventory<br /> \nCustomer Bills<br />\nExpenses<br />\nCannot Navigate Multiple Shops', '2022-09-13 22:44:25', 0, '2022-09-25 13:14:13', NULL),
(4, 'DIRECTOR', 4, 'View Reports Only<br /> \nCan Navigate Multiple Shops', '2022-09-13 22:44:25', 0, '2022-09-25 13:14:14', NULL);

-- Table structure for table `users`
CREATE TABLE IF NOT EXISTS `users` (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  phone TEXT UNIQUE NOT NULL,
  shop_id INTEGER NOT NULL,
  user_level_id INTEGER NOT NULL,
  password TEXT NOT NULL,
  created_at TEXT NOT NULL,
  created_by INTEGER NOT NULL,
  updated_at TEXT,
  updated_by INTEGER,
  FOREIGN KEY (user_level_id) REFERENCES user_levels(id)
);
