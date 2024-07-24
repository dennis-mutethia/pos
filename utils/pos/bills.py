from datetime import datetime
from flask import render_template, request
from flask_login import current_user

from utils.entities import Bill
from utils.pos.customers import Customers
from utils.pos.payments import Payments

class Bills():
    def __init__(self, db): 
        self.db = db
            
    def fetch(self, report_date, bill_status):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, total, paid, created_at, customer_id, created_by
            FROM bills
            WHERE DATE(created_at) = DATE(%s) AND shop_id = %s
            """
            params = [report_date, current_user.shop.id]
            
            if bill_status==1:
                query = query + " AND paid>=total"
            if bill_status==2:
                query = query + " AND paid<=total"
            
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            bills = []
            for datum in data:                
                customer = Customers(self.db).fetch_by_id(datum[4])
                user = self.db.get_user_by_id(datum[5])  
                payments = Payments(self.db).fetch_by_bill_id(datum[0])         
                bills.append(Bill(datum[0], datum[1], datum[2], datum[3], customer, user, payments))

            return bills 
               
    def fetch_by_id(self, id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, total, paid, created_at, customer_id, created_by
            FROM bills
            WHERE id = %s
            """
            params = [id]
            
            cursor.execute(query, tuple(params))
            data = cursor.fetchone()
            if data:
                customer = Customers(self.db).fetch_by_id(data[4])
                user = self.db.get_user_by_id(data[5])
                payments = Payments(self.db).fetch_by_bill_id(data[0])
                return Bill(data[0], data[1], data[2], data[3], customer, user, payments)
            else:
                return None    
      
    def add(self, customer_id, amount_paid):
        self.db.ensure_connection()            
        query = """
        WITH temp_bill AS(
            SELECT %s AS customer_id, SUM(price*qty) AS total, %s AS paid, %s AS shop_id, NOW() AS created_at, %s AS created_by
            FROM bill_entries
            WHERE shop_id = %s AND bill_id=0 AND created_by = %s
        )
        INSERT INTO bills(customer_id, total, paid, shop_id, created_at, created_by) 
        SELECT * FROM temp_bill
        RETURNING id
        """

        params = (customer_id, amount_paid, current_user.shop.id, current_user.id, current_user.shop.id, current_user.id)
        try:
            with self.db.conn.cursor() as cursor:
                cursor.execute(query, tuple(params))
                self.db.conn.commit()
                row_id = cursor.fetchone()[0]
                return row_id
        except Exception as e:
            self.db.conn.rollback()
            raise e
        
    def __call__(self):
        current_date = datetime.now().strftime('%Y-%m-%d')
        report_date = current_date
        bill_status = 0 
        
        if request.method == 'GET':   
            try:    
                report_date = request.args.get('report_date', datetime.now().strftime('%Y-%m-%d'))
                bill_status = int(request.args.get('bill_status', 0))
            except ValueError as e:
                print(f"Error converting bill_status: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
                
        if request.method == 'POST':       
            if request.form['action'] == 'add':
                stock_id = request.form['stock_id']    
                bill_id = request.form['bill_id']
                item_name = request.form['item_name']    
                price = request.form['price']       
                qty = request.form['qty']    
                #self.add(bill_id, stock_id, item_name, price, qty)
                return 'success'                
                
            elif request.form['action'] == 'delete':
                id = request.form['item_id']
                #self.delete(id) 
                
        bills = self.fetch(report_date, bill_status) 
        grand_total = grand_paid = cash_total = mpesa_total =  0
        for bill in bills:
            grand_total = grand_total + bill.total
            grand_paid = grand_paid + bill.paid
            cash_total = cash_total + bill.cash
            mpesa_total = mpesa_total + bill.mpesa
            
        return render_template('pos/bills.html', page_title='POS > Bills', bills=bills, current_date=current_date, bill_status=bill_status, report_date=report_date,
                               grand_total=grand_total, grand_paid=grand_paid, cash_total=cash_total, mpesa_total=mpesa_total )