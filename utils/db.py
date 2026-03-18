import os, psycopg2, pytz, uuid
from flask_login import current_user
from datetime import datetime, timedelta

from utils.entities import Company, License, Package, PaymentMode, Shop, ShopType, User, UserLevel
from utils.helper import Helper

class Db:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        self.conn = None
        self.ensure_connection()

    def ensure_connection(self):
        """
        Ensure a valid DB connection; reconnect if broken
        """
        try:
            if self.conn is None or self.conn.closed:
                self.conn = psycopg2.connect(self.database_url)
            else:
                with self.conn.cursor() as cur:
                    cur.execute("SELECT 1")
        except Exception:
            try:
                if self.conn:
                    self.conn.close()
            except:
                pass
            self.conn = psycopg2.connect(self.database_url)

    # Context manager for safe cursor usage
    def cursor(self):
        self.ensure_connection()
        return self.conn.cursor()

    # ----------------------
    # Generic execute helper
    # ----------------------
    def execute(self, query, params=None, fetchone=False, fetchall=False, commit=True):
        self.ensure_connection()
        with self.conn.cursor() as cur:
            cur.execute(query, params or ())
            result = None
            if fetchone:
                result = cur.fetchone()
            elif fetchall:
                result = cur.fetchall()
            if commit:
                self.conn.commit()
            return result

    # ----------------------
    # Your existing methods
    # ----------------------
    def create_base_tables(self):
        try:
            self.ensure_connection()
            with open("pos.sql", "r") as f:
                sql_script = f.read()
            with self.conn.cursor() as cursor:
                cursor.execute(sql_script)
                self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error executing SQL script: {e}")

    def load_shop_template_data(self, shop_id):        
        query1 = """
        INSERT INTO product_categories(name, shop_id, created_at, created_by)
        SELECT name, %s, NOW(), %s FROM product_categories WHERE shop_id = 0
        """
        self.execute(query1, (shop_id, current_user.id))
        
        query2 = """
        INSERT INTO products(name, purchase_price, selling_price, category_id, shop_id, created_at, created_by)
        SELECT name, purchase_price, selling_price, category_id, %s, NOW(), %s FROM products WHERE shop_id = 0
        """
        self.execute(query2, (shop_id, current_user.id))

    def save_payment(self, bill_id, amount, payment_mode_id):
        query = """
        INSERT INTO payments(bill_id, amount, payment_mode_id, created_at, created_by) 
        VALUES(%s, %s, %s, NOW(), 0) 
        RETURNING id
        """
        return self.execute(query, (bill_id, amount, payment_mode_id), fetchone=True)[0]

    def save_license(self, package, payment_id):
        key = str(uuid.uuid4())
        query = """
        INSERT INTO licenses(key, package_id, payment_id, expires_at, created_at, created_by) 
        VALUES(%s, %s, %s, NOW() + INTERVAL %s, NOW(), 0)
        RETURNING id
        """
        return self.execute(query, (key, package.id, payment_id, f'+{package.validity} DAYS'), fetchone=True)[0]

    def save_company(self, name, license_id):
        query = """
        INSERT INTO companies(name, license_id, created_at, created_by) 
        VALUES(%s, %s, NOW(), 0) 
        RETURNING id
        """
        return self.execute(query, (name.upper(), license_id), fetchone=True)[0]

    def get_license_by_id(self, id):
        query = """
        SELECT id, key, package_id, DATE(expires_at), expires_at > NOW(), EXTRACT(DAY FROM (expires_at - NOW()))
        FROM licenses 
        WHERE id = %s
        """
        data = self.execute(query, (id,), fetchone=True)
        if data:
            return License(*data)
        return None

    def get_company_by_id(self, id):
        query = "SELECT id, name, license_id FROM companies WHERE id = %s"
        data = self.execute(query, (id,), fetchone=True)
        if data:
            return Company(*data)
        return None

    def get_company_shops(self):
        query = """
        SELECT id, name, shop_type_id, company_id, location, phone_1, phone_2, paybill, account_no, till_no
        FROM shops 
        WHERE company_id = %s
        """
        data = self.execute(query, (current_user.company.id,), fetchall=True)
        return [Shop(*d) for d in data]

    def get_package_by_id(self, id):
        query = """
        SELECT id, name, amount, description, color, validity, pay
        FROM packages 
        WHERE id = %s
        """
        data = self.execute(query, (id,), fetchone=True)
        if data:
            return Package(*data)
        return None

    def fetch_payment_modes(self):
        data = self.execute("SELECT id, name, account FROM payment_modes", fetchall=True)
        return [PaymentMode(*d) for d in data]

    def get_payment_mode_by_id(self, id):
        query = "SELECT id, name, account FROM payment_modes WHERE id = %s"
        data = self.execute(query, (id,), fetchone=True)
        if data:
            return PaymentMode(*data)
        return None

    def create_current_month_partition(self):        
        current_date = datetime.now(pytz.timezone("Africa/Nairobi")).replace(day=1)
        next_month = (current_date + timedelta(days=31)).replace(day=1)
        partition_name = f"stock_{current_date.year}_{current_date.month:02d}"
        query = f"""
        CREATE TABLE IF NOT EXISTS {partition_name} PARTITION OF stock
        FOR VALUES FROM ('{current_date.strftime("%Y-%m-%d")}') 
        TO ('{next_month.strftime("%Y-%m-%d")}')
        """
        self.execute(query)
        print(f"Partition {partition_name} created successfully.")