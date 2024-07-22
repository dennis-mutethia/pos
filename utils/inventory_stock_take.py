from flask import render_template, request
from flask_login import current_user
from datetime import datetime

from utils.entities import Stock
from utils.inventory_products_categories import InventoryProductsCategories

class InventoryStockTake():
    def __init__(self, db): 
        self.db = db
                    
    def load(self, stock_date):
        self.db.ensure_connection()
        
        # Ensure current_user is accessible and properly imported or passed
        from flask_login import current_user
        
        with self.db.conn.cursor() as cursor:
            query = """
            WITH p AS (
                SELECT id, name, category_id, purchase_price, selling_price
                FROM products 
                WHERE shop_id = %s
            ),
            yesterday AS (
                SELECT product_id, name, category_id, purchase_price, selling_price, opening, additions, (opening+additions) AS closing
                FROM stock
                WHERE DATE(stock_date) = DATE(%s) - 1
            ),
            today AS (
                SELECT DATE(%s) AS stock_date, 
                    COALESCE(yesterday.product_id, p.id) AS product_id, 
                    COALESCE(yesterday.name, p.name) AS name, 
                    COALESCE(yesterday.category_id, p.category_id) AS category_id,
                    COALESCE(yesterday.purchase_price, p.purchase_price) AS purchase_price,
                    COALESCE(yesterday.selling_price, p.selling_price) AS selling_price,
                    COALESCE(yesterday.closing, 0) AS opening,
                    COALESCE(yesterday.additions, 0) AS additions,
                    %s AS shop_id, NOW() AS created_at, %s AS created_by              
                FROM p
                LEFT JOIN yesterday ON yesterday.product_id = p.id
            )
            INSERT INTO stock (stock_date, product_id, name, category_id, purchase_price, selling_price, opening, additions, shop_id, created_at, created_by) 
            SELECT * FROM today
            ON CONFLICT (stock_date, product_id, shop_id) DO NOTHING
            RETURNING id
            """
            params = [current_user.shop_id, stock_date, stock_date, current_user.shop_id, current_user.id]
            
            try:
                cursor.execute(query, tuple(params))
                self.db.conn.commit()
                id = cursor.fetchone()[0]
                return id
            except Exception as e:
                self.db.conn.rollback()
                print(f"Error loading stock: {e}")
                return None
    
    def fetch(self, stock_date, search, category_id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            #id, product_id, name, category_name, yesterday, opening, additions, sold
            query = """
            WITH all_stock AS(
                SELECT id, stock_date, product_id, name, category_id, opening, additions
                FROM stock 
                WHERE shop_id = %s
            ),
            yesterday AS (
                SELECT product_id, opening
                FROM all_stock
                WHERE DATE(stock_date) = DATE(%s) - 1
            ), 
            today AS(
                SELECT id, product_id, name, category_id, opening, additions
                FROM all_stock
                WHERE DATE(stock_date) = DATE(%s)
            )
            SELECT today.id, today.product_id, today.name, product_categories.name, COALESCE(yesterday.opening,0), today.opening, today.additions, 0 AS sold
            FROM today
            INNER JOIN product_categories ON product_categories.id = today.category_id
            LEFT JOIN yesterday ON yesterday.product_id = today.product_id
            WHERE today.id > 0
            """
            params = [current_user.shop_id, stock_date, stock_date]

            if search:
                query += " AND today.name LIKE %s"
                params.append(f"%{search.upper()}%")
            if int(category_id) > 0:
                query += " AND today.category_id = %s"
                params.append(category_id)
            
            query = query + " ORDER BY today.category_id, today.name"
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            stocks = []
            for stock in data:
                stocks.append(Stock(stock[0], stock[1], stock[2], stock[3], stock[4], stock[5], stock[6], stock[7]))

            return stocks
            
    def update(self, id, name, purchase_price, selling_price, opening, additions):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            UPDATE stock
            SET name=%s, purchase_price=%s, selling_price=%s, opening=%s, additions=%s, updated_at=NOW(), updated_by=%s
            WHERE id=%s
            """
            params = [name.upper(), purchase_price, selling_price, opening, additions, current_user.id, id]
            cursor.execute(query, tuple(params))
            self.db.conn.commit()
            
    def delete(self, id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            DELETE FROM stock
            WHERE id=%s
            """
            cursor.execute(query, (id,))
            self.db.conn.commit()
             
    def __call__(self):
        search = ''
        category_id = 0   
        current_date = datetime.now().strftime('%Y-%m-%d')
        stock_date = current_date   
        if request.method == 'GET':   
            try:    
                search = request.args.get('search', '')
                category_id = int(request.args.get('category_id', 0))
                stock_date = request.args.get('stock_date', default=current_date)
                self.load(stock_date)                
            except ValueError as e:
                print(f"Error converting category_id: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
        
        if request.method == 'POST':       
            if request.form['action'] == 'update':
                id = request.form['id']
                name = request.form['name']    
                purchase_price = request.form['purchase_price']
                selling_price = request.form['selling_price']     
                opening = request.form['opening']
                additions = request.form['additions']     
                self.update(id, name, purchase_price, selling_price, opening, additions)
                return 'success'
                
            elif request.form['action'] == 'delete':
                id = request.form['item_id']
                self.delete(id) 
               
        shop = self.db.get_shop_by_id(current_user.shop_id) 
        company = self.db.get_company_by_id(shop.company_id)
        license = self.db.get_license_id(company.license_id)
        
        product_categories = InventoryProductsCategories(self.db).fetch_product_categories()
        stocks = self.fetch(stock_date, search, category_id)
        return render_template('inventory/stock-take.html', shop=shop, company=company, license=license, product_categories=product_categories, stocks=stocks, 
                               page_title='Stock Take', stock_date=stock_date, current_date=current_date, search=search, category_id=category_id)
