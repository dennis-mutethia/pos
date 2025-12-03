from datetime import datetime
import pytz

from utils.db import Db
                    
def load_stock(stock_date):        
    db = Db()
    
    query = """         
        WITH sales AS(
            SELECT stock_id, SUM(qty) sold
            FROM bill_entries
            WHERE bill_id>0
            GROUP BY stock_id
        ),
        p AS (
            SELECT id, name, category_id, purchase_price, selling_price
            FROM products 
        ),
        yesterday AS (
            SELECT product_id, name, category_id, purchase_price, selling_price, opening, additions, COALESCE(sold, 0) AS sold, stock.shop_id
            FROM stock
            LEFT JOIN sales ON sales.stock_id = stock.id
            WHERE DATE(stock_date) = DATE(%s) - 1
        ),
        today AS (
            SELECT DATE(%s) AS stock_date, 
                COALESCE(yesterday.product_id, p.id) AS product_id, 
                COALESCE(yesterday.name, p.name) AS name, 
                COALESCE(yesterday.category_id, p.category_id) AS category_id,
                COALESCE(yesterday.purchase_price, p.purchase_price) AS purchase_price,
                COALESCE(yesterday.selling_price, p.selling_price) AS selling_price,
                COALESCE((yesterday.opening+yesterday.additions-yesterday.sold), 0) AS opening,
                0 AS additions,
                yesterday.shop_id AS shop_id, 
                NOW() AS created_at, 
                0 AS created_by              
            FROM p
            LEFT JOIN yesterday ON yesterday.product_id = p.id
        )
        INSERT INTO stock (stock_date, product_id, name, category_id, purchase_price, selling_price, opening, additions, shop_id, created_at, created_by) 
        SELECT * FROM today
        ON CONFLICT (stock_date, product_id, shop_id) DO NOTHING
    """
    
    params = [stock_date, stock_date]
    
    with db.conn.cursor() as cursor:               
        cursor.execute(query, tuple(params))
        db.conn.commit()
    

if __name__ == '__main__':
    current_date = datetime.now(pytz.timezone("Africa/Nairobi")).strftime('%Y-%m-%d')
    load_stock(stock_date=current_date)