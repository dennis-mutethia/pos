from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import secrets

from utils.db import Db

app = Flask(__name__)
secret_key = secrets.token_hex()
app.secret_key = secret_key
login_manager = LoginManager()
login_manager.init_app(app)
app.app_context().push()

db = Db()
#db.create_base_tables()
         
# Callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return db.get_user_by_id(user_id)

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    shop_types = db.fetch_shop_types()

    error = None
    if request.method == 'POST':
        if request.form['action'] == 'login':
            phone = request.form['phone']
            password = request.form['password']   
            user = db.authenticate_user(phone, password)
            
            if user: 
                login_user(user)
                return redirect(url_for('dashboard'))
            else: 
                error = 'Login failed! Phone & Password do not match or Phone does not exist.'
                
        if request.form['action'] == 'register':
            company_name = request.form['company_name']
            shop_name = request.form['shop_name']  
            shop_type_id = request.form['shop_type_id']
            shop_location = request.form['shop_location'] 
            user_name = request.form['user_name']    
            user_phone = request.form['user_phone']
            user_password = request.form['user_password'] 
            
            package = db.get_package_by_id(1)
            payment_id = db.save_payment(0, 0, 4)
            license_id = db.save_license(package, payment_id)
            company_id = db.save_company(company_name, license_id)
            shop_id = db.save_shop(shop_name, shop_type_id, company_id, shop_location)
            user = db.get_user_by_phone(user_phone)
            if user is None:
                user_id = db.save_user(user_name, user_phone, 1, shop_id, user_password)
                user = db.get_user_by_id(user_id)
            else:
                db.update_user(user.id, user_name, user_password, shop_id)
                    
            login_user(user)
            return redirect(url_for('dashboard'))

    return render_template('login.html', shop=None, shop_types=shop_types, error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    shop = db.get_shop_by_id(current_user.shop_id) 
    company = db.get_company_by_id(shop.company_id)
    license = db.get_license_id(company.license_id)
    
    if request.method == 'POST':       
        website_name = request.form['website_name']
        website_url = request.form['website_url']  
    
    return render_template('dashboard.html', shop=shop, company=company, license=license, page_title='Dashboard')

@app.route('/dashboard/<int:website_id>/delete', methods=['POST'])
@login_required
def delete(website_id):

    # TODO 4: Implement the function for deleting websites from user profiles.
    
    delete_website(website_id)
    return redirect(url_for("dashboard"))

if __name__ == '__main__':
    app.run(debug=True)
