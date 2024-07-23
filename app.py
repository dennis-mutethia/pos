import os
from flask import Flask, render_template, request, redirect, url_for
from flask_caching import Cache
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from dotenv import load_dotenv
from flask_session import Session
from redis import Redis

from utils.dashboard import Dashboard
from utils.db import Db
from utils.inventory_products import InventoryProducts
from utils.inventory_products_categories import InventoryProductsCategories
from utils.inventory_purchases import InventoryPurchases
from utils.inventory_stock_adjustment import InventoryStockAdjustment
from utils.inventory_stock_take import InventoryStockTake
from utils.login import Login

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # One year in seconds

# Configure caching
cache = Cache(config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})
cache.init_app(app)

# Load environment variables from .env file
load_dotenv()
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
    return InventoryProductsCategories(db)()

@app.route('/inventory-products', methods=['GET', 'POST'])
@login_required
def inventoryProducts():
    return InventoryProducts(db)()

@app.route('/inventory-products-update', methods=['POST'])
@login_required
def inventoryProductsUpdate():    
    return InventoryProducts(db)()

@app.route('/inventory-stock-take', methods=['GET', 'POST'])
@login_required
def inventoryStockTake():
    return InventoryStockTake(db)()

@app.route('/inventory-stock-take-update', methods=['POST'])
@login_required
def inventoryStockTakeUpdate():    
    return InventoryStockTake(db)()

@app.route('/inventory-purchases', methods=['GET', 'POST'])
@login_required
def inventoryPurchases():
    return InventoryPurchases(db)()

@app.route('/inventory-purchases-update', methods=['POST'])
@login_required
def inventoryPurchasesUpdate():
    return InventoryPurchases(db)()

@app.route('/inventory-stock-adjustment', methods=['GET', 'POST'])
@login_required
def inventoryStockAdjustment():
    return InventoryStockAdjustment(db)()

@app.route('/inventory-stock-adjustment-update', methods=['POST'])
@login_required
def inventoryStockAdjustmentUpdate():
    return InventoryStockAdjustment(db)()

if __name__ == '__main__':
    debug_mode = os.getenv('IS_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)
