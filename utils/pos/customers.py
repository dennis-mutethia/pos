from datetime import datetime
from flask import render_template, request
from flask_login import current_user

from utils.entities import Customer
from utils.inventory.products_categories import ProductsCategories
from utils.inventory.stock_take import StockTake

class Customers():
    def __init__(self, db): 
        self.db = db
    
    def fetch(self):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            #$id, $name, $selling_price, remaining, $temp_qty
            query = """
            SELECT id, name, phone
            FROM customers
            WHERE shop_id=%s 
            ORDER BY name
            """
            params = [current_user.shop.id]
            
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            stocks = []
            for stock in data:
                #id, name, selling_price, actual, temp_qty
                stocks.append(Customer(stock[0], stock[1], stock[2]))

            return stocks
        
    def __call__(self):
        search = ''
        category_id = 0  
        page = 1   
        if request.method == 'GET':   
            try:    
                search = request.args.get('search', '')
                category_id = int(request.args.get('category_id', 0))
                page = int(request.args.get('page', 1))
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
                self.add(name, purchase_price, selling_price, category_id)
                StockTake(self.db).load(datetime.now().strftime('%Y-%m-%d'))
            
            elif request.form['action'] == 'update':
                id = request.form['id']
                name = request.form['name']    
                purchase_price = request.form['purchase_price']
                selling_price = request.form['selling_price']    
                self.update(id, name, purchase_price, selling_price)
                return 'success'
                
            elif request.form['action'] == 'delete':
                id = request.form['item_id']
                self.delete(id) 
        
        product_categories = ProductsCategories(self.db).fetch()
        products = self.fetch(search, category_id, page)
        prev_page = page-1 if page>1 else 0
        next_page = page+1 if len(products)==30 else 0
        return render_template('pos/customers.html', product_categories=product_categories, products=products, 
                               page_title='POS > Customers', search=search, category_id=category_id, page=page, prev_page=prev_page, next_page=next_page )
