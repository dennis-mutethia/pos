from flask import render_template, request
from flask_login import current_user, login_required

class Dashboard():
    def __init__(self, db): 
        self.db = db
    
    @login_required  
    def __call__(self):
        shop = self.db.get_shop_by_id(current_user.shop_id) 
        company = self.db.get_company_by_id(shop.company_id)
        license = self.db.get_license_id(company.license_id)
        
        return render_template('dashboard/index.html', shop=shop, company=company, license=license, page_title='Dashboard')