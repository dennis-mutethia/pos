from flask import render_template, request
from flask_login import current_user

from utils.entities import Bill, BillEntry

class Bills():
    def __init__(self, db): 
        self.db = db
            
    def fetch(self, bill_id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, customer_id, total, paid, created_at, created_by
            FROM bills
            WHERE id = %s
            """
            params = [bill_id]
            
            cursor.execute(query, tuple(params))
            data = cursor.fetchone()
            if data:
                user = self.db.get_user_by_id(data[5])
                return Bill(data[0], data[1], data[2], data[3], data[4], user)
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
        if request.method == 'POST':       
            if request.form['action'] == 'add':
                stock_id = request.form['stock_id']    
                bill_id = request.form['bill_id']
                item_name = request.form['item_name']    
                price = request.form['price']       
                qty = request.form['qty']    
                self.add(bill_id, stock_id, item_name, price, qty)
                return 'success'                
                
            elif request.form['action'] == 'delete':
                id = request.form['item_id']
                self.delete(id) 
                
        bill_entries = self.fetch(0)
        grandtotal = 0
        for bill_entry in bill_entries:
            grandtotal = grandtotal + (bill_entry.price * bill_entry.qty) 
            
        return render_template('pos/bill-entries.html', bill_entries=bill_entries, grandtotal=grandtotal )