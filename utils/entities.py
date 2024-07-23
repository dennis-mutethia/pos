from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, name, phone, user_level, shop, company, license):  
        self.id = id
        self.name = name
        self.phone = phone
        self.user_level = user_level
        self.shop = shop 
        self.company = company 
        self.license = license

class UserLevel():
    def __init__(self, id, name, level, description):
        self.id = id
        self.name = name
        self.name = level
        self.description = description 
        
class ShopType():
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description
    
class License():
    def __init__(self, id, key, package_id, expires_at, is_valid):
        self.id = id
        self.key = key
        self.package_id = package_id
        self.expires_at = expires_at
        self.is_valid = is_valid
    
class Company():
    def __init__(self, id, name, license_id):
        self.id = id
        self.name = name
        self.license_id = license_id
        
class Shop():
    def __init__(self, id, name, shop_type_id, company_id, location, phone_1, phone_2, paybill, account_no, till_no):
        self.id = id
        self.name = name
        self.shop_type_id = shop_type_id
        self.company_id = company_id
        self.company = None
        self.location = location
        self.phone_1 = phone_1
        self.phone_2 = phone_2
        self.paybill = paybill
        self.account_no = account_no
        self.till_no = till_no

class Package():
    def __init__(self, id, name, amount, description, color, validity):
        self.id = id
        self.name = name
        self.amount = amount
        self.description = description
        self.color = color
        self.validity = validity

class ProductCategory():
    def __init__(self, id, name, products_count):
        self.id = id
        self.name = name    
        self.products_count = products_count   

class Product():
    def __init__(self, id, name, purchase_price, selling_price, category_id):
        self.id = id
        self.name = name    
        self.purchase_price = purchase_price   
        self.selling_price = selling_price    
        self.category_id = category_id   

class Stock():
    def __init__(self, id, product_id, name, category_name, yesterday, opening, additions, sold):
        self.id = id 
        self.product_id = product_id   
        self.name = name     
        self.category_name = category_name   
        self.yesterday = yesterday 
        self.opening = opening   
        self.additions = additions     
        self.sold = sold  

class InStock():
    def __init__(self, id, name, selling_price, actual, temp_qty):
        self.id = id    
        self.name = name     
        self.selling_price = selling_price   
        self.actual = actual 
        self.temp_qty = temp_qty   