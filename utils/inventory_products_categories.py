from flask import render_template, request
from flask_login import current_user

from utils.entities import ProductCategories

class InventoryProductsCategories():
    def __init__(self, db): 
        self.db = db
    
    def fetch_product_categories(self):
        self.db.ensure_connection() 
        with self.db.conn.cursor() as cursor:
            query = """
            WITH p AS(
                SELECT shop_id, category_id, COUNT(*) counts FROM products GROUP BY shop_id, category_id
            )
            SELECT id, name, COALESCE(counts, 0)
            FROM product_categories 
            LEFT JOIN p ON p.category_id = product_categories.id AND p.shop_id = product_categories.shop_id
            WHERE product_categories.shop_id = %s
            ORDER BY name
            """
            cursor.execute(query, (current_user.shop_id,))
            data = cursor.fetchall()
            product_categories = []
            for shop_type in data:
                product_categories.append(ProductCategories(shop_type[0], shop_type[1], shop_type[2]))
                
            return product_categories 
    
    def save_product_category(self, name):
        self.db.ensure_connection()
        with self.conn.cursor() as cursor:
            query = """
            INSERT INTO product_categories(name, shop_id, created_at, created_by) 
            VALUES(%s, %s, NOW(), %s) 
            ON CONFLICT (name, shop_id) DO NOTHING
            RETURNING id
            """
            cursor.execute(query, (name.upper(), current_user.shop_id, current_user.id))
            self.db.conn.commit()
            id = cursor.fetchone()[0]
            return id   
            
    def update_product_category(self, id, name):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            UPDATE product_categories
            SET name=%s, updated_at=NOW(), updated_by=%s
            WHERE id=%s
            """
            params = [name.upper(), current_user.shop_id, current_user.id]
            cursor.execute(query, tuple(params))
            self.db.conn.commit()
            
    def delete_product_category(self, id):
        self.db.ensure_connection()
        with self.conn.cursor() as cursor:
            query = """
            DELETE FROM product_categories
            WHERE id=%s
            """
            print(query)
            cursor.execute(query, (id,))
            self.db.conn.commit()
            
    def __call__(self):
        shop = self.db.get_shop_by_id(current_user.shop_id) 
        company = self.db.get_company_by_id(shop.company_id)
        license = self.db.get_license_id(company.license_id)
        
        if request.method == 'POST':       
            if request.form['action'] == 'add':
                name = request.form['name']
                self.save_product_category(name)   
                
            elif request.form['action'] == 'update':
                id = request.form['id']
                name = request.form['name']    
                self.update_product_category(id, name)
                return 'success'
                   
            elif request.form['action'] == 'delete':
                id = request.form['item_id']
                self.delete_product_category(id) 
        
        product_categories = self.fetch_product_categories()
        return render_template('inventory/products-categories.html', shop=shop, company=company, license=license, product_categories=product_categories, page_title='Product Categories')
