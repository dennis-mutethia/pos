from flask import render_template, request
from flask_login import current_user

class Dashboard():
    def __init__(self, db): 
        self.db = db
        
    def __call__(self):
        
        return render_template('dashboard/index.html', page_title='Dashboard')