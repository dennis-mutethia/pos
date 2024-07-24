from flask import render_template, request
from flask_login import current_user

from utils.entities import BillEntry, Customer
from utils.pos.bill_entries import BillEntries
from utils.pos.bills import Bills
from utils.pos.payments import Payments

class Print():
    def __init__(self, db): 
        self.db = db
            
    def fetch_customer(self, bill_id):                                 
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            #$id, $name, $selling_price, remaining, $temp_qty
            query = """
            SELECT customers.id, customers.name, customers.phone
            FROM bills
            JOIN customers ON customers.id = bills.customer_id
            WHERE bills.id = %s
            """
            params = [bill_id]
            
            cursor.execute(query, tuple(params))
            data = cursor.fetchone()
            if data:
                #id, name, selling_price, actual, temp_qty
                return Customer(data[0], data[1], data[2])
            else:
                return None      
            
    def __call__(self):   
        bill_id = int(request.args.get('bill_id', 0))
        show_vat = int(request.args.get('show_vat', 0))
                     
        customer = self.fetch_customer(bill_id)
        bill = Bills(self.db).fetch(bill_id)
        bill_entries = BillEntries(self.db).fetch(bill_id)
        payments = Payments(self.db).fetch(bill_id)
            
        return render_template('pos/print.html', customer=customer, bill_id=bill_id, show_vat=show_vat, 
                               bill=bill, bill_entries=bill_entries, payments=payments )