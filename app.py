import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from dotenv import load_dotenv
from flask_session import Session
from redis import Redis

from utils.db import Db
# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = r = Redis(
    host=os.getenv('REDIS_HOSTNAME'),
    port=os.getenv('REDIS_PORT'),
    password=os.getenv('REDIS_PASSWORD'),
    ssl=True
)
app.config['SESSION_COOKIE_SECURE'] = True  # Set to True if using HTTPS on Vercel
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

Session(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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
                
        elif request.form['action'] == 'register':
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
            
            #db.load_shop_template_data(shop_id)
                   
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
    
    return render_template('dashboard/index.html', shop=shop, company=company, license=license, page_title='Dashboard')

@app.route('/inventory-products-categories', methods=['GET', 'POST'])
@login_required
def inventoryProductsCategories():
    shop = db.get_shop_by_id(current_user.shop_id) 
    company = db.get_company_by_id(shop.company_id)
    license = db.get_license_id(company.license_id)
    
    if request.method == 'POST':       
        if request.form['action'] == 'add':
            name = request.form['name']
            product_category_id = db.save_product_category(name)      
        elif request.form['action'] == 'delete':
            id = request.form['item_id']
            db.delete_product_category(id) 
    
    product_categories = db.fetch_product_categories()
    return render_template('inventory/products-categories/index.html', shop=shop, company=company, license=license, product_categories=product_categories, page_title='Product Categories')

@app.route('/inventory-products-categories-update', methods=['POST'])
@login_required
def inventoryProductsCategoriesUpdate():    
    if request.method == 'POST':       
        if request.form['action'] == 'update':
            id = request.form['item_id']
            name = request.form['name']    
            db.update_product_category(id, name)
            
    return 'success'

@app.route('/dashboard/<int:website_id>/delete', methods=['POST'])
@login_required
def delete(website_id):

    # TODO 4: Implement the function for deleting websites from user profiles.
    
    delete_website(website_id)
    return redirect(url_for("dashboard"))

if __name__ == '__main__':
    app.run(debug=True)
