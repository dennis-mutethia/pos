from datetime import datetime
from flask import render_template, request
from flask_login import current_user

from utils.expenses import Expenses
from utils.helper import Helper
from utils.inventory.stock_take import StockTake
from utils.pos.bill_entries import BillEntries
from utils.pos.bills import Bills

class Dashboard():
    def __init__(self, db): 
        self.db = db
        
    def __call__(self):
        current_date = datetime.now().strftime('%Y-%m-%d')
        report_date = current_date
        
        if request.method == 'GET':   
            try:    
                report_date = request.args.get('report_date', current_date)
                
            except Exception as e:
                print(f"An error occurred: {e}")
        
        total_cost, total_sales = BillEntries(self.db).get_total(report_date)
        total_expenses = Expenses(self.db).get_total(report_date)
        total_capital, total_stock = StockTake(self.db).get_total(report_date)
        total_unpaid_bills = Bills(self.db).get_total_unpaid_bills()
         
        return render_template('dashboard/index.html', page_title='Dashboard', report_date=report_date, helper=Helper(),
                               total_cost=total_cost, total_sales=total_sales, total_expenses=total_expenses,
                               total_capital=total_capital, total_stock=total_stock, total_unpaid_bills=total_unpaid_bills )