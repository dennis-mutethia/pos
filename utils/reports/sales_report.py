from datetime import datetime
from flask import render_template, request
from flask_login import current_user

from utils.entities import Sale
from utils.helper import Helper
from utils.inventory.products_categories import ProductsCategories

class SalesReport():
    def __init__(self, db): 
        self.db = db

    def fetch(self, from_date, to_date, category_id=0, page=0):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT DATE(be.created_at) AS report_date, be.item_name, pc.name AS category_name, s.selling_price, SUM(COALESCE(be.qty,0)) sold 
            FROM bill_entries be
            JOIN stock s ON s.id=be.stock_id
            LEFT JOIN product_categories pc ON pc.id= s.category_id   
            WHERE (DATE(be.created_at) BETWEEN DATE(%s) AND DATE(%s)) AND be.shop_id = %s AND be.bill_id>0            
            """
            params = [from_date, to_date, current_user.shop.id]
            
            if category_id > 0:
                query = query + " AND s.category_id = %s "
                params.append(category_id)
            
            query = query + """
            GROUP BY report_date, be.item_name, pc.name, s.selling_price
            ORDER BY report_date DESC, sold DESC
            """
            
            if page>0:
                query = query + """
                LIMIT 50 OFFSET %s
                """
                params.append((page - 1)*50)
            
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            sales = []
            for datum in data:                       
                sales.append(Sale(datum[0], datum[1], datum[2], datum[3], datum[4]))

            return sales 
         
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
        
        sales = self.fetch(from_date, to_date, category_id, page) 
        prev_page = page-1 if page>1 else 0
        next_page = page+1 if len(sales)==50 else 0
        grand_total =  0
        for sale in sales:
            total = sale.selling_price * sale.sold
            grand_total = grand_total + total
        
        product_categories = ProductsCategories(self.db).fetch()
        return render_template('reports/sales-report.html', page_title='Reports > Sales', helper=Helper(), menu='reports', sub_menu='sales_report',
                               sales=sales, grand_total=grand_total, product_categories=product_categories, category_id=category_id,
                               current_date=current_date, from_date=from_date, to_date=to_date,
                                page=page, prev_page=prev_page, next_page=next_page)