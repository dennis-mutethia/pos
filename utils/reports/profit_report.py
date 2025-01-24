from datetime import datetime
from flask import render_template, request
from flask_login import current_user

from utils.entities import Profit
from utils.helper import Helper

class ProfitReport():
    def __init__(self, db): 
        self.db = db
   
    def fetch(self, from_date, to_date):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            WITH exp AS(
                SELECT date, SUM(amount) total_expenses
                FROM expenses
                GROUP BY date
            ),
            sales AS(
                SELECT DATE(b.created_at) AS report_date, be.price*be.qty AS sales, s.purchase_price*be.qty AS cost
                FROM bills b
                JOIN bill_entries be ON be.bill_id = b.id
                JOIN stock s ON s.id = be.stock_id 
                WHERE DATE(b.created_at) BETWEEN DATE(%s) AND DATE(%s) AND b.shop_id=%s AND total != 'Nan'
            ),
            totals AS(
                SELECT report_date, SUM(sales) AS total_sales, SUM(cost) AS total_cost
                FROM sales  
                GROUP BY report_date
            )
            SELECT report_date, total_sales, total_cost, COALESCE(total_expenses,0) AS total_expenses
            FROM totals
            LEFT JOIN exp ON exp.date=totals.report_date    
            ORDER BY report_date     
            """
            params = [from_date, to_date, current_user.shop.id]
            
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            profits = []
            for datum in data:                
                profits.append(Profit(datum[0], datum[1], datum[2], datum[3]))

            return profits 
         
    def __call__(self):
        current_date = datetime.now().strftime('%Y-%m-%d')
        from_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        to_date = current_date
        page = 1
        download = 0
        
        if request.method == 'GET':   
            try:    
                from_date = request.args.get('from_date', from_date)
                to_date = request.args.get('to_date', to_date)
                page = int(request.args.get('page', 1))
                download = int(request.args.get('download', download))
            except Exception as e:
                print(f"An error occurred: {e}")               
        
        profits = self.fetch(from_date, to_date) 
        prev_page = page-1 if page>1 else 0
        next_page = page+1 if len(profits)==50 else 0
                        
        return render_template('reports/profit-report.html', page_title='Reports > Profit & Loss', helper=Helper(), menu='reports', sub_menu='profit_report',
                               profits=profits, from_date=from_date, to_date=to_date, current_date=current_date,
                               page=page, prev_page=prev_page, next_page=next_page
                               )