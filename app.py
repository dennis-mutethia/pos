import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from dotenv import load_dotenv
from flask_session import Session
from redis import Redis

from utils.dashboard import Dashboard
from utils.db import Db
from utils.inventory.products import Products
from utils.inventory.products_categories import ProductsCategories
from utils.inventory.purchases import Purchases
from utils.inventory.stock_adjustment import StockAdjustment
from utils.inventory.stock_take import StockTake
from utils.login import Login
from utils.pos.bill_entries import BillEntries
from utils.pos.new_sale import NewSale
from utils.pos.print import Print

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # One year in seconds

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
    return ProductsCategories(db)()

@app.route('/inventory-products-categories-update', methods=['POST'])
@login_required
def inventoryProductsCategoriesUpdate():    
    return ProductsCategories(db)()

@app.route('/inventory-products', methods=['GET', 'POST'])
@login_required
def inventoryProducts():
    return Products(db)()

@app.route('/inventory-products-update', methods=['POST'])
@login_required
def inventoryProductsUpdate():    
    return Products(db)()

@app.route('/inventory-stock-take', methods=['GET', 'POST'])
@login_required
def inventoryStockTake():
    return StockTake(db)()

@app.route('/inventory-stock-take-update', methods=['POST'])
@login_required
def inventoryStockTakeUpdate():    
    return StockTake(db)()

@app.route('/inventory-purchases', methods=['GET', 'POST'])
@login_required
def inventoryPurchases():
    return Purchases(db)()

@app.route('/inventory-purchases-update', methods=['POST'])
@login_required
def inventoryPurchasesUpdate():
    return Purchases(db)()

@app.route('/inventory-stock-adjustment', methods=['GET', 'POST'])
@login_required
def inventoryStockAdjustment():
    return StockAdjustment(db)()

@app.route('/inventory-stock-adjustment-update', methods=['POST'])
@login_required
def inventoryStockAdjustmentUpdate():
    return StockAdjustment(db)()

@app.route('/pos-new-sale', methods=['GET', 'POST'])
@login_required
def posNewSale():
    return NewSale(db)()

@app.route('/pos-bill-entries', methods=['GET'])
@login_required
def posBillEntries():
    return BillEntries(db)()

@app.route('/pos-bill-entries-update', methods=['POST'])
@login_required
def posBillEntriesUpdate():
    return BillEntries(db)()

@app.route('/pos-print', methods=['GET'])
@login_required
def posPrint():
    return Print(db)()

if __name__ == '__main__':
    debug_mode = os.getenv('IS_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)
