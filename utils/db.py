from flask_login import current_user
import sqlite3, hashlib, os, uuid, psycopg2
from flask import current_app

from utils.entities import Company, License, Package, ProductCategories, Shop, ShopType, User

class Db():
    def __init__(self):
        # Access the environment variables
        self.conn_params = {
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME'),
            'port': os.getenv('DB_PORT'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
        
        self.conn = None
        self.ensure_connection()
    
    def ensure_connection(self):
        try:
            # Check if the connection is open
            if self.conn is None or self.conn.closed:
                self.conn = psycopg2.connect(**self.conn_params)
            else:
                # Test the connection
                with self.conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
        except Exception as e:
            # Reconnect if the connection is invalid
            self.conn = psycopg2.connect(**self.conn_params)
               
    def hash_password(self, password):
        password_bytes = password.encode('utf-8')
        hash_object = hashlib.sha256(password_bytes)
        return hash_object.hexdigest()
    
    def create_base_tables(self):
        self.ensure_connection()
        # Creates new tables in the pos.db database if they do not already exist.
        with current_app.open_resource("pos.sql") as f:
            with self.conn.cursor() as cursor:
                cursor.executescript(f.read().decode("utf8"))
                self.conn.commit()
    
    def load_shop_template_data(self, shop_id):        
        self.ensure_connection()
        with self.conn.cursor() as cursor:
            query = """
            INSERT INTO product_categories(name, shop_id, created_at, created_by)
            SELECT name, ?, NOW(), ? FROM product_categories WHERE shop_id = 0
            """
            cursor.execute(query, (shop_id, current_user.id))
            self.conn.commit()            
            
            query = """
            INSERT INTO products(name, purchase_price, selling_price, category_id, shop_id, created_at, created_by)
            SELECT name, purchase_price, selling_price, category_id, ?, NOW(), ? FROM products WHERE shop_id = 0
            """
            cursor.execute(query, (shop_id, current_user.id))
            self.conn.commit()
            
    def fetch_shop_types(self):
        self.ensure_connection() 
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT id, name, description FROM shop_types")
            data = cursor.fetchall()
            shop_types = []
            for shop_type in data:
                shop_types.append(ShopType(shop_type[0], shop_type[1], shop_type[2]))
                
            return shop_types    
    
    def get_user_by_id(self, id):
        self.ensure_connection()
        with self.conn.cursor() as cursor:
            query = """
            SELECT id, name, phone, user_level_id, shop_id
            FROM users 
            WHERE id = %s 
            """
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            if data:
                return User(data[0], data[1], data[2], data[3], data[4])
            else:
                return None      
    
    def get_user_by_phone(self, phone):
        self.ensure_connection()
        with self.conn.cursor() as cursor:
            query = """
            SELECT id, name, phone, user_level_id, shop_id
            FROM users 
            WHERE phone = %s 
            """
            cursor.execute(query, (phone,))
            data = cursor.fetchone()
            if data:
                return User(data[0], data[1], data[2], data[3], data[4])
            else:
                return None    
           
    def authenticate_user(self, phone, password):
        self.ensure_connection()
        with self.conn.cursor() as cursor:
            query = """
            SELECT id, name, phone, user_level_id, shop_id
            FROM users 
            WHERE phone = %s AND password = %s 
            """
            cursor.execute(query, (phone, self.hash_password(password)))
            data = cursor.fetchone()
            if data:
                return User(data[0], data[1], data[2], data[3], data[4])
            else:
                return None 
    
    def save_user(self, name, phone, user_level_id, shop_id, password):
        self.ensure_connection()
        with self.conn.cursor() as cursor:
            query = """
            INSERT INTO users(name, phone, user_level_id, shop_id, password, created_at, created_by) 
            VALUES(%s, %s, %s, %s, %s, NOW(), 0)
            RETURNING id
            """
            cursor.execute(query, (name.upper(), phone, user_level_id, shop_id, self.hash_password(password)))
            self.conn.commit()
            user_id = cursor.fetchone()[0]
            return user_id   
    
    def save_payment(self, bill_id, amount, payment_mode_id):
        self.ensure_connection()
        with self.conn.cursor() as cursor:
            query = """
            INSERT INTO payments(bill_id, amount, payment_mode_id, created_at, created_by) 
            VALUES(%s, %s, %s, NOW(), 0) 
            RETURNING id
            """
            cursor.execute(query, (bill_id, amount, payment_mode_id))
            self.conn.commit()
            payment_id = cursor.fetchone()[0]
            return payment_id 
    
    def save_license(self, package, payment_id):
        self.ensure_connection()
        with self.conn.cursor() as cursor:
            key = uuid.uuid4()
            query = """
            INSERT INTO licenses(key, package_id, payment_id, expires_at, created_at, created_by) 
            VALUES(%s, %s, %s, NOW() + INTERVAL %s, NOW(), 0)
            RETURNING id
            """
            cursor.execute(query, (str(key), package.id, payment_id, f'+{package.validity} DAYS'))
            self.conn.commit()
            license_id = cursor.fetchone()[0]
            return license_id
    
    def save_company(self, name, license_id):
        self.ensure_connection()
        with self.conn.cursor() as cursor:
            query = """
            INSERT INTO companies(name, license_id, created_at, created_by) 
            VALUES(%s, %s, NOW(), 0) 
            RETURNING id
            """
            cursor.execute(query, (name.upper(), license_id))
            self.conn.commit()
            company_id = cursor.fetchone()[0]
            return company_id 
    
    def save_shop(self, name, shop_type_id, company_id, location):
        self.ensure_connection()
        with self.conn.cursor() as cursor:
            query = """
            INSERT INTO shops(name, shop_type_id, company_id, location, created_at, created_by) 
            VALUES(%s, %s, %s, %s, NOW(), 0) 
            RETURNING id
            """
            cursor.execute(query, (name.upper(), shop_type_id, company_id, location.upper()))
            self.conn.commit()
            shop_id = cursor.fetchone()[0]
            return shop_id
    
    def delete_website(self, website_id):
        self.ensure_connection()
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM websites WHERE id = %s', (website_id,))
        conn.commit()
        conn.close() 
      
    def get_license_id(self, id):
        self.ensure_connection()
        with self.conn.cursor() as cursor:
            query = """
            SELECT id, key, package_id, expires_at, expires_at > NOW() as is_valid
            FROM licenses 
            WHERE id = %s 
            """
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            if data:
                return License(data[0], data[1], data[2], data[3], data[4])
            else:
                return None    
      
    def get_company_by_id(self, id):
        self.ensure_connection()
        with self.conn.cursor() as cursor:
            query = """
            SELECT id, name, license_id
            FROM companies 
            WHERE id = %s 
            """
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            if data:
                return Company(data[0], data[1], data[2])
            else:
                return None    
      
    def get_shop_by_id(self, id):
        self.ensure_connection()
        with self.conn.cursor() as cursor:
            query = """
            SELECT id, name, shop_type_id, company_id, location, phone_1, phone_2, paybill, account_no, till_no
            FROM shops 
            WHERE id = %s 
            """
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            if data:
                return Shop(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9])
            else:
                return None    
        
    def get_package_by_id(self, id):
        self.ensure_connection()
        with self.conn.cursor() as cursor:
            query = """
            SELECT id, name, amount, description, color, validity
            FROM packages 
            WHERE id = %s 
            """
            cursor.execute(query, (id,))
            data = cursor.fetchone()
            if data:
                return Package(data[0], data[1], data[2], data[3], data[4], data[5])
            else:
                return None    
            
    def update_user(self, user_id, name, password, shop_id):
        self.ensure_connection()
        with self.conn.cursor() as cursor:
            query = """
            UPDATE users 
            SET name = %s, password = %s, shop_id = %s, updated_by=%s, updated_at=NOW() 
            WHERE id=%s
            """
            cursor.execute(query, (name.upper(), self.hash_password(password), shop_id, user_id, user_id))
            self.conn.commit()
    
    def fetch_product_categories(self):
        self.ensure_connection() 
        with self.conn.cursor() as cursor:
            query = """
            WITH p AS(
                SELECT shop_id, category_id, COUNT(*) counts FROM products GROUP BY shop_id, category_id
            )
            SELECT id, name, COALESCE(counts, 0)
            FROM product_categories 
            LEFT JOIN p ON p.category_id = product_categories.id AND p.shop_id = product_categories.shop_id
            WHERE product_categories.shop_id = %s
            """
            cursor.execute(query, (current_user.shop_id,))
            data = cursor.fetchall()
            product_categories = []
            for shop_type in data:
                product_categories.append(ProductCategories(shop_type[0], shop_type[1], shop_type[2]))
                
            return product_categories 
    
    def save_product_category(self, name):
        self.ensure_connection()
        with self.conn.cursor() as cursor:
            query = """
            INSERT INTO product_categories(name, shop_id, created_at, created_by) 
            VALUES(%s, %s, NOW(), %s) 
            RETURNING id
            """
            cursor.execute(query, (name.upper(), current_user.shop_id, current_user.id))
            self.conn.commit()
            id = cursor.fetchone()[0]
            return id   
            
    def delete_product_category(self, id):
        self.ensure_connection()
        with self.conn.cursor() as cursor:
            query = """
            DELETE FROM product_categories
            WHERE id=%s
            """
            cursor.execute(query, (id,))
            self.conn.commit()
            
    def update_product_category(self, id, name):
        self.ensure_connection()
        with self.conn.cursor() as cursor:
            query = """
            UPDATE product_categories
            SET name=%s
            WHERE id=%s
            """
            cursor.execute(query, (name.upper(), id))
            self.conn.commit()
        