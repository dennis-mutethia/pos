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
    return Dashboard(db)() 

@app.route('/inventory-products-categories', methods=['GET', 'POST'])
@login_required
def inventoryProductsCategories():
    return InventoryProductsCategories(db)() 

@app.route('/inventory-products-categories-update', methods=['POST'])
@login_required
def inventoryProductsCategoriesUpdate():    
    return InventoryProductsCategories(db).update()

if __name__ == '__main__':
    app.run(debug=True)
