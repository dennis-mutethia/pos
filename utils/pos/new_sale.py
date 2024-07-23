from datetime import datetime
from flask import render_template, request
from flask_login import current_user

from utils.entities import InStock
from utils.inventory.products_categories import ProductsCategories
from utils.inventory.stock_take import StockTake
from utils.pos.customers import Customers

class NewSale():
    def __init__(self, db): 
        self.db = db
    
    def fetch(self, search, category_id, page, in_stock):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            #$id, $name, $selling_price, remaining, $temp_qty
            query = """
            SELECT id, name, selling_price, (opening+additions) AS actual, 0 AS temp_qty
            FROM stock
            WHERE shop_id=%s AND DATE(stock_date) = CURRENT_DATE AND (opening+additions) >= %s
            """
            params = [current_user.shop.id, in_stock]

            if search:
                query += " AND name LIKE %s"
                params.append(f"%{search.upper()}%")
            if int(category_id) > 0:
                query += " AND category_id = %s"
                params.append(category_id)
            
            query = query + """
            ORDER BY category_id, name
            LIMIT 30 OFFSET %s            
            """
            params.append((page - 1)*30)
            
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            stocks = []
            for stock in data:
                #id, name, selling_price, actual, temp_qty
                stocks.append(InStock(stock[0], stock[1], stock[2], stock[3], stock[4]))

            return stocks
        
    def __call__(self):
        search = ''
        category_id = 0  
        page = 1   
        in_stock = 0
        if request.method == 'GET':   
            try:    
                search = request.args.get('search', '')
                category_id = int(request.args.get('category_id', 0))
                page = int(request.args.get('page', 1))
                in_stock = int(request.args.get('in_stock', 0))
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
        
        product_categories = ProductsCategories(self.db).fetch()
        products = self.fetch(search, category_id, page, in_stock)
        customers = Customers(self.db).fetch()
        prev_page = page-1 if page>1 else 0
        next_page = page+1 if len(products)==30 else 0
        return render_template('pos/new-sale.html', product_categories=product_categories, products=products, customers=customers, in_stock=in_stock,
                               page_title='POS > New Sale', search=search, category_id=category_id, page=page, prev_page=prev_page, next_page=next_page )
