from flask import render_template, request
from flask_login import current_user

from utils.entities import Payment
from utils.helper import Helper
from utils.settings.system_users import SystemUsers

class OurPackages():
    def __init__(self, db): 
        self.db = db
          
    def __call__(self):
        toastr_message = None   
        package_id = current_user.license.package_id
        package = self.db.get_package_by_id(package_id)  
            
        return render_template('packages.html', page_title='Our Packages', helper=Helper(),
                               package = package, toastr_message = toastr_message)