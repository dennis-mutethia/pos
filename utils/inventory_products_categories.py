from flask import render_template, request

class InventoryProductsCategories():
    def __init__(self, db): 
        self.db = db               
        
    def __call__(self):        
        if request.method == 'POST':       
            if request.form['action'] == 'add':
                name = request.form['name']
                self.db.save_product_category(name)      
            elif request.form['action'] == 'delete':
                id = request.form['item_id']
                self.db.delete_product_category(id) 
            elif request.form['action'] == 'update':
                id = request.form['item_id']
                name = request.form['name']    
                self.db.update_product_category(id, name)
                return 'success'