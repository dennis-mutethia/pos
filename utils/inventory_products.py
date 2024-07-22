from flask import render_template, request
from flask_login import current_user

class InventoryProducts():
    def __init__(self, db): 
        self.db = db

    def __call__(self):
        search = ''
        category_id = 0        
        if request.method == 'GET':   
            try:    
                search = request.args.get('search', '')
                category_id = int(request.args.get('category_id', 0))
            except ValueError as e:
                print(f"Error converting category_id: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
        
        if request.method == 'POST':       
            if request.form['action'] == 'add':
                name = request.form['name']    
                purchase_price = request.form['purchase_price']
                selling_price = request.form['selling_price']    
                category_id = request.form['category_id_new']    
                self.db.save_product(name, purchase_price, selling_price, category_id)
            
            elif request.form['action'] == 'update':
                id = request.form['id']
                name = request.form['name']    
                purchase_price = request.form['purchase_price']
                selling_price = request.form['selling_price']    
                self.db.update_product(id, name, purchase_price, selling_price)
                return 'success'
                
            elif request.form['action'] == 'delete':
                id = request.form['item_id']
                self.db.delete_product(id) 
                
        shop = self.db.get_shop_by_id(current_user.shop_id) 
        company = self.db.get_company_by_id(shop.company_id)
        license = self.db.get_license_id(company.license_id)
        
        product_categories = self.db.fetch_product_categories()
        products = self.db.fetch_products(search, category_id)
        return render_template('inventory/products.html', shop=shop, company=company, license=license, product_categories=product_categories, products=products, 
                               page_title='Product Categories', search=search, category_id=category_id)
