from flask import render_template, request
from flask_login import current_user, login_required

class Dashboard():
    def __init__(self, db): 
        self.db = db
    
    @login_required  
    def __call__(self):
        print(None)