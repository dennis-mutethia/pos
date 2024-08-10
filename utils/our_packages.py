from flask import render_template, request
from flask_login import current_user

from utils.entities import Payment
from utils.helper import Helper
from utils.settings.system_users import SystemUsers

class OurPackages():
    def __init__(self, db): 
        self.db = db
            
    def fetch(self):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT id, bill_id, amount, payment_mode_id, created_at, created_by
            FROM payments
            WHERE bill_id = %s
            """
            params = [bill_id]
            
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()
            payments = []
            for datum in data:
                payment_mode = self.db.get_payment_mode_by_id(datum[3])
                user = SystemUsers(self.db).get_by_id(datum[5])                
                payments.append(Payment(datum[0], datum[1], datum[2], datum[4], user, payment_mode))

            return payments 
             
    def __call__(self):
        toastr_message = None     
            
        return render_template('packages.html', page_title='Our Packages', helper=Helper(),
                               toastr_message = toastr_message)