from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import secrets

from utils.dashboard import Dashboard
from utils.db import Db
from utils.login import Login
from utils.inventory_products_categories import InventoryProductsCategories

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
    return Login(db)()

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard(): 
    Dashboard(db)() 
    shop = db.get_shop_by_id(current_user.shop_id) 
    company = db.get_company_by_id(shop.company_id)
    license = db.get_license_id(company.license_id)
    
    return render_template('dashboard/index.html', shop=shop, company=company, license=license, page_title='Dashboard')

@app.route('/inventory-products-categories', methods=['GET', 'POST'])
@login_required
def inventoryProductsCategories():
    InventoryProductsCategories(db)()
    
    shop = db.get_shop_by_id(current_user.shop_id) 
    company = db.get_company_by_id(shop.company_id)
    license = db.get_license_id(company.license_id)
    product_categories = db.fetch_product_categories()
    
    return render_template('inventory/products-categories/index.html', shop=shop, company=company, license=license, product_categories=product_categories, page_title='Product Categories')

@app.route('/inventory-products-categories-update', methods=['POST'])
@login_required
def inventoryProductsCategoriesUpdate():    
    return InventoryProductsCategories(db)()

if __name__ == '__main__':
    app.run(debug=True)
