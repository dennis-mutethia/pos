from datetime import datetime
from flask import redirect, render_template, request, url_for
from flask_login import login_user

from utils.inventory.stock_take import StockTake

class Login():
    def __init__(self, db): 
        self.db = db
           
    def login(self):  
        if request.method == 'POST':
            if request.form['action'] == 'login':
                phone = request.form['phone']
                password = request.form['password']   
                user = self.db.authenticate_user(phone, password)
                
                if user:        
                    login_user(user)
                    StockTake(self.db).load(datetime.now().strftime('%Y-%m-%d'))
                    return redirect(url_for('dashboard'))
                else: 
                    error = 'Login failed! Phone & Password do not match or Phone does not exist.'
                    shop_types = self.db.fetch_shop_types()
                    return render_template('login.html', shop_types=shop_types, error=error)
    
    def register(self):           
        company_name = request.form['company_name']
        shop_name = request.form['shop_name']  
        shop_type_id = request.form['shop_type_id']
        shop_location = request.form['shop_location'] 
        user_name = request.form['user_name']    
        user_phone = request.form['user_phone']
        user_password = request.form['user_password'] 
        
        package = self.db.get_package_by_id(1)
        payment_id = self.db.save_payment(0, 0, 4)
        license_id = self.db.save_license(package, payment_id)
        company_id = self.db.save_company(company_name, license_id)
        shop_id = self.db.save_shop(shop_name, shop_type_id, company_id, shop_location)
        user = self.db.get_user_by_phone(user_phone)
        if user is None:
            user_id = self.db.save_user(user_name, user_phone, 1, shop_id, user_password)
            user = self.db.get_user_by_id(user_id)
        else:
            self.db.update_user(user.id, user_name, user_password, shop_id)
                    
        login_user(user)
        StockTake(self.db).load(datetime.now().strftime('%Y-%m-%d'))                
        return redirect(url_for('dashboard'))
      
    def __call__(self):
        if request.method == 'POST':
            if request.form['action'] == 'register':
                return self.register()
            elif request.form['action'] == 'login':
                return self.login()

        shop_types = self.db.fetch_shop_types()
        return render_template('login.html', shop=None, shop_types=shop_types, error=None)
