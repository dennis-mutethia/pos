from flask import render_template, request
from flask_login import current_user

from utils.entities import Products
from utils.inventory_products_categories import InventoryProductsCategories

class InventoryProducts():
    def __init__(self, db): 
        self.db = db
    
    def fetch_products(self, search, category_id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, name, purchase_price, selling_price, category_id
            FROM products
            WHERE shop_id = %s
            """
            params = [current_user.shop_id]

            if search:
                query += " AND name LIKE %s"
                params.append(f"%{search.upper()}%")
            if int(category_id) > 0:
                query += " AND category_id = %s"
                params.append(category_id)
            
            query = query + " ORDER BY category_id, name"
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            products = []
            for product in data:
                products.append(Products(product[0], product[1], product[2], product[3], product[4]))

            return products
                    
    def save_product(self, name, purchase_price, selling_price, category_id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            INSERT INTO products(name, purchase_price, selling_price, category_id, shop_id, created_at, created_by) 
            VALUES(%s, %s, %s, %s, %s, NOW(), %s) 
            ON CONFLICT (name, shop_id) DO NOTHING
            RETURNING id
            """
            params = [name.upper(), purchase_price, selling_price, category_id, current_user.shop_id, current_user.id]
            cursor.execute(query, tuple(params))
            self.db.conn.commit()
            id = cursor.fetchone()[0]
            return id   
            
    def update_product(self, id, name, purchase_price, selling_price):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            UPDATE products
            SET name=%s, purchase_price=%s, selling_price=%s, updated_at=NOW(), updated_by=%s
            WHERE id=%s
            """
            params = [name.upper(), purchase_price, selling_price, current_user.id, id]
            cursor.execute(query, tuple(params))
            self.db.conn.commit()
            
    def delete_product(self, id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            DELETE FROM products
            WHERE id=%s
            """
            cursor.execute(query, (id,))
            self.db.conn.commit()
        
        
    def __call__(self):
        search = ''
        category_id = 0        
        if request.method == 'GET':   
            try:    
                search = request.args.get('search', '')
                category_id = int(request.args.get('category_id', 0))
            except ValueError as e:
                print(f"Error converting category_id: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
        
        if request.method == 'POST':       
            if request.form['action'] == 'add':
                name = request.form['name']    
                purchase_price = request.form['purchase_price']
                selling_price = request.form['selling_price']    
                category_id = request.form['category_id_new']    
                self.save_product(name, purchase_price, selling_price, category_id)
            
            elif request.form['action'] == 'update':
                id = request.form['id']
                name = request.form['name']    
                purchase_price = request.form['purchase_price']
                selling_price = request.form['selling_price']    
                self.update_product(id, name, purchase_price, selling_price)
                return 'success'
                
            elif request.form['action'] == 'delete':
                id = request.form['item_id']
                self.delete_product(id) 
                
        shop = self.db.get_shop_by_id(current_user.shop_id) 
        company = self.db.get_company_by_id(shop.company_id)
        license = self.db.get_license_id(company.license_id)
        
        product_categories = InventoryProductsCategories(self.db).fetch_product_categories()
        products = self.fetch_products(search, category_id)
        return render_template('inventory/products.html', shop=shop, company=company, license=license, product_categories=product_categories, products=products, 
                               page_title='Product Categories', search=search, category_id=category_id)
