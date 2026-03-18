import os
from flask import Flask, redirect, render_template, url_for, request
from flask_login import LoginManager, login_required
from dotenv import load_dotenv

from utils.jwt_manager import JWTManager
from utils.refresh_token_manager import RefreshTokenManager

from utils.account_profile import AccountProfile
from utils.our_packages import OurPackages
from utils.customers.customer_bills import CustomerBills
from utils.customers.customers import Customers
from utils.dashboard import Dashboard
from utils.db import Db
from utils.expenses import Expenses
from utils.inventory.products import Products
from utils.inventory.products_categories import ProductsCategories
from utils.inventory.purchases import Purchases
from utils.inventory.stock_adjustment import StockAdjustment
from utils.inventory.stock_take import StockTake
from utils.login import Login
from utils.pos.bill_details import BillDetails
from utils.pos.bill_entries import BillEntries
from utils.pos.bills import Bills
from utils.pos.new_sale import NewSale
from utils.pos.print import Print
from utils.reports.bills_report import BillsReport
from utils.reports.expenses_report import ExpensesReport
from utils.reports.profit_report import ProfitReport
from utils.reports.purchases_report import PurchasesReport
from utils.reports.sales_report import SalesReport
from utils.reports.statement_of_account import StatementOfAccount
from utils.reports.stock_report import StockReport
from utils.settings.companies import Companies
from utils.settings.company_shops import CompanyShops
from utils.settings.my_shops import MyShops
from utils.settings.system_users import SystemUsers

app = Flask(__name__)
load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = Db()
refresh_manager = RefreshTokenManager(db)

# 🔥 JWT-based loader
@login_manager.request_loader
def load_user_from_request(request):
    token = request.cookies.get("access_token")

    if not token:
        return None

    user_id = JWTManager.verify_access_token(token)

    if not user_id:
        return None

    return SystemUsers(db).get_by_id(user_id)


# 🔄 Auto refresh middleware
@app.before_request
def refresh_expired_token():
    token = request.cookies.get("access_token")

    if token and JWTManager.verify_access_token(token):
        return

    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return

    result = refresh_manager.verify(refresh_token)

    if not result:
        return

    # Issue new access token
    new_access = JWTManager.generate_access_token(result["user_id"])

    from flask import g
    g.new_access_token = new_access


@app.after_request
def attach_new_token(response):
    from flask import g

    if hasattr(g, "new_access_token"):
        response.set_cookie(
            "access_token",
            g.new_access_token,
            httponly=True,
            secure=True,
            samesite="Lax"
        )
    return response


# Routes (UNCHANGED)
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return Login(db, refresh_manager)()

@app.route('/logout')
@login_required
def logout():
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token:
        refresh_manager.delete(refresh_token)

    response = redirect(url_for('login'))
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return response

# ---- all your other routes remain EXACTLY the same ----

if __name__ == '__main__':
    debug_mode = os.getenv('IS_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)