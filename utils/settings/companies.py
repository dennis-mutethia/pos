from flask import redirect, render_template, request, url_for
from flask_login import current_user

from utils.entities import Shop
from utils.helper import Helper

class Company():
    def __init__(self, id, name, phone, created_at, license_key, expires_at, package, validity):
        self.id = id
        self.name = name
        self.phone = phone
        self.created_at = created_at
        self.license_key = license_key
        self.expires_at = expires_at
        self.package = package
        self.validity = validity
        
class Companies():
    def __init__(self, db): 
        self.db = db
            
    def fetch(self):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            SELECT c.id, c.name, u.phone, DATE(c.created_at), l.key, DATE(l.expires_at), p.name, EXTRACT(DAY FROM (l.expires_at - NOW()))
            FROM companies c
            LEFT JOIN users u ON u.id = c.created_by
            JOIN licenses l ON l.id = c.license_id
            JOIN packages p ON p.id = l.package_id
            """
            #params = [current_user.company.id]
            
            cursor.execute(query)
            data = cursor.fetchall()
            companies = []
            for datum in data:   
                companies.append(Company(datum[0], datum[1], datum[2], datum[3], datum[4], datum[5], datum[6], datum[7]))

            return companies 
       
    def update(self, shop_id, name, shop_type_id, company_id, location, phone_1, phone_2, paybill, account_no, till_no, updated_by):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            UPDATE shops 
            SET name = %s, shop_type_id = %s, company_id = %s, location = %s, phone_1 = %s, phone_2 = %s, paybill = %s, account_no = %s, till_no = %s, updated_at=NOW(), updated_by = %s 
            WHERE id = %s          
            """
            cursor.execute(query, (name.upper(), shop_type_id, company_id, location.upper(), phone_1, phone_2, paybill, account_no, till_no, updated_by, shop_id))
            self.db.conn.commit()
            
    def delete(self, id):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            DELETE FROM shops
            WHERE id = %s
            """
            cursor.execute(query, (id,))
            self.db.conn.commit()
        
    def __call__(self):   
        toastr_message = None             
        if request.method == 'POST':       
            if request.form['action'] == 'update':  
                name = request.form['name']
                location = request.form['location']      
                shop_type_id = request.form['shop_type_id']   
                company_id = current_user.company.id  
                phone_1 = request.form['phone_1']       
                phone_2 = request.form['phone_2']       
                paybill = request.form['paybill']       
                account_no = request.form['account_no']       
                till_no = request.form['till_no']    
                created_by = current_user.id 
                
                shop_id = request.form['shop_id']
                self.update(shop_id, name, shop_type_id, company_id, location, phone_1, phone_2, paybill, account_no, till_no, created_by)
                toastr_message = f'{name} Updated Successfully'
                                
            elif request.form['action'] == 'delete':
                shop_id = request.form['shop_id']
                self.delete(shop_id)
                toastr_message = f'Shop Deleted Successfully'
        
        companies = self.fetch() 
            
        return render_template('settings/companies.html', page_title='Companies', helper=Helper(),
                               companies=companies, toastr_message=toastr_message )