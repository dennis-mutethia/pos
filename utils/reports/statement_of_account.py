from datetime import datetime
from flask import render_template, request
from flask_login import current_user

from utils.entities import Statement
from utils.helper import Helper

class StatementOfAccount():
    def __init__(self, db): 
        self.db = db
            
    def fetch(self, from_date, to_date):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            WITH sales AS(
                SELECT DATE(created_at) AS date, SUM(total) AS sales,0 AS purchases,0 AS expenses
                FROM bills
                WHERE DATE(created_at) BETWEEN DATE(%s) AND DATE(%s) AND shop_id=%s AND total != 'Nan'
                GROUP BY date
            ),            
            purchases AS(
                SELECT stock_date,0,SUM(additions*purchase_price), 0
                FROM stock
                WHERE stock_date BETWEEN DATE(%s) AND DATE(%s) AND shop_id = %s
                GROUP BY stock_date
            ),
            expenses AS(
                SELECT date,0,0,SUM(amount)
                FROM expenses
                WHERE date BETWEEN DATE(%s) AND DATE(%s) AND shop_id = %s
                GROUP BY date
            ),
            final AS(
                SELECT * FROM sales
                UNION SELECT * FROM purchases
                UNION SELECT * FROM expenses
            )
            SELECT * FROM final 
            ORDER BY date ASC, sales DESC, purchases DESC, expenses DESC
            """
            params = [
                from_date, to_date, current_user.shop.id,
                from_date, to_date, current_user.shop.id,
                from_date, to_date, current_user.shop.id
            ]
            
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            statements = []
            for datum in data:                   
                statements.append(Statement(datum[0], datum[1], datum[2], datum[3]))

            return statements 
         
    def __call__(self):
        current_date = datetime.now().strftime('%Y-%m-%d')
        from_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        to_date = current_date
        download = 0
        
        if request.method == 'GET':   
            try:    
                from_date = request.args.get('from_date', from_date)
                to_date = request.args.get('to_date', to_date)
                page = int(request.args.get('page', 1))
                download = int(request.args.get('download', download))
            except Exception as e:
                print(f"An error occurred: {e}")               
        
        statements = self.fetch(from_date, to_date) 
                    
        return render_template('reports/statement-of-account.html', page_title='Reports >Statement of Account', helper=Helper(),
                               statements=statements, from_date=from_date, to_date=to_date, current_date=current_date
                               )