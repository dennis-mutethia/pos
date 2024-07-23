from flask import render_template, request
from flask_login import current_user

from utils.entities import BillEntry

class BillEntries():
    def __init__(self, db): 
        self.db = db
            
    def fetch(self):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            #$id, $name, $selling_price, remaining, $temp_qty
            query = """
            SELECT id, bill_id, stock_id, item_name, price, qty
            FROM bill_entries
            WHERE shop_id=%s 
            ORDER BY id
            """
            params = [current_user.shop.id]
            
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            bill_entries = []
            for bill_entry in data:
                #id, name, selling_price, actual, temp_qty
                bill_entries.append(BillEntry(bill_entry[0], bill_entry[1], bill_entry[2], bill_entry[3], bill_entry[4], bill_entry[5]))

            return bill_entries
            
    def add(self, bill_id, stock_id, item_name, price, qty):
        self.db.ensure_connection()
        
        query = """
        INSERT INTO bill_entries(bill_id, stock_id, item_name, price, qty, shop_id, created_at, created_by) 
        VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s) 
        ON CONFLICT (bill_id, stock_id, created_by) DO UPDATE 
        SET qty = EXCLUDED.qty, updated_at = NOW(), updated_by = %s
        RETURNING id
        """

        params = (bill_id, stock_id, item_name.upper(), price, qty, current_user.shop.id, current_user.id, current_user.id)

        try:
            with self.db.conn.cursor() as cursor:
                cursor.execute(query, params)
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
                
        bill_entries = self.fetch()
        grandtotal = 0
        for bill_entry in bill_entries:
            grandtotal = grandtotal + (bill_entry.price * bill_entry.qty) 
            
        return render_template('pos/bill-entries.html', bill_entries=bill_entries, grandtotal=grandtotal )