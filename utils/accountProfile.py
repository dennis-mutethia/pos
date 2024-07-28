from flask import render_template, request
from flask_login import current_user

from utils.helper import Helper

class AccountProfile():
    def __init__(self, db): 
        self.db = db
            
    def update(self, name, phone, password):
        self.db.ensure_connection()
        with self.db.conn.cursor() as cursor:
            query = """
            UPDATE users
            SET name=%s, phone=%s, password=%s, updated_at=NOW(), updated_by=%s
            WHERE id=%s
            """
            params = [name.upper(), phone, Helper().hash_password(password), current_user.id, current_user.id]
            cursor.execute(query, tuple(params))
            self.db.conn.commit()
             
    def __call__(self):
        toastr_message = None
                
        if request.method == 'POST':       
            if request.form['action'] == 'update':
                name = request.form['name']
                phone = request.form['phone']    
                password = request.form['password']                
                self.update(name, phone, password)  
                toastr_message = 'Profile Updated Successfully'        
            
        return render_template('account-profile.html', page_title='My Account Profile', helper=Helper(),
                               toastr_message = toastr_message)