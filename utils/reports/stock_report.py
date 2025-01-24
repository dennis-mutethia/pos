from datetime import datetime
from flask import render_template, request
from flask_login import current_user

from utils.helper import Helper
from utils.inventory.products_categories import ProductsCategories

class Stock():
    def __init__(self, stock_date, name, category_name, opening, additions, sold, selling_price):
        self.stock_date = stock_date
        self.name = name
        self.category_name = category_name
        self.opening = opening
        self.additions = additions
        self.sold = sold
        self.selling_price = selling_price
        
class StockReport():
    def __init__(self, db): 
        self.db = db

    def fetch(self, from_date, to_date, category_id=0, page=0):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """ 
            WITH sales AS(
                SELECT stock_id, SUM(qty) sold
                FROM bill_entries
                WHERE shop_id = %s AND bill_id>0
                GROUP BY stock_id
            )
            SELECT stock_date, stock.name, product_categories.name AS category_name, stock.opening, stock.additions, COALESCE(sales.sold, 0) AS sold, stock.selling_price
            FROM stock 
            LEFT JOIN sales ON sales.stock_id = stock.id
            LEFT JOIN product_categories ON product_categories.id= stock.category_id
            WHERE (DATE(stock.created_at) BETWEEN DATE(%s) AND DATE(%s)) AND stock.shop_id = %s
            """
            params = [current_user.shop.id, from_date, to_date, current_user.shop.id]
            
            if category_id > 0:
                query = query + " AND stock.category_id = %s "
                params.append(category_id)
            
            query = query + """
            ORDER BY stock_date DESC, category_name, name
            """
            
            if page>0:
                query = query + """
                LIMIT 50 OFFSET %s
                """
                params.append((page - 1)*50)
            
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            stocks = []
            for datum in data:                    
                stocks.append(Stock(datum[0], datum[1], datum[2], datum[3], datum[4], datum[5], datum[6]))

            return stocks 
         
    def __call__(self):
        current_date = datetime.now().strftime('%Y-%m-%d')
        from_date = to_date = current_date
        category_id = 0
        page = 1
        download = 0
        
        if request.method == 'GET':   
            try:    
                from_date = request.args.get('from_date', from_date)
                to_date = request.args.get('to_date', to_date)
                category_id = int(request.args.get('category_id', 0))
                page = int(request.args.get('page', 1))
                download = int(request.args.get('download', download))
            except Exception as e:
                print(f"An error occurred: {e}")               
        
        stocks = self.fetch(from_date, to_date, category_id, page) 
        prev_page = page-1 if page>1 else 0
        next_page = page+1 if len(stocks)==50 else 0
        grand_total =  0
        for stock in stocks:
            total = stock.selling_price * stock.sold
            grand_total = grand_total + total
       
        product_categories = ProductsCategories(self.db).fetch()
        return render_template('reports/stock-report.html', page_title='Reports > Stock', helper=Helper(),
                               stocks=stocks, grand_total=grand_total, product_categories=product_categories, category_id=category_id,
                               current_date=current_date, from_date=from_date, to_date=to_date,
                                page=page, prev_page=prev_page, next_page=next_page)