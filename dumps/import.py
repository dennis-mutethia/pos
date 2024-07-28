import os, psycopg2

from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()

# Database connection details
database_url = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
conn_string = f"dbname={os.getenv('DB_NAME')} user={os.getenv('DB_USER')} password={os.getenv('DB_PASSWORD')} host={os.getenv('DB_HOST')} port={os.getenv('DB_PORT')}"
chunk_size = 10000

def  import_csv():
    tables = ['bill_entries']
    for table in tables:
        # File path to the CSV file
        csv_file_path = f'29_{table}.csv'

        # Table name where data will be inserted
        table_name = f'{table}_29'

        # Create an SQLAlchemy engine for database connection
        engine = create_engine(database_url)

        # Process CSV in chunks and upload to the database
        try:
            # Read the CSV file in chunks
            for chunk in pd.read_csv(csv_file_path, chunksize=chunk_size):
                # Upload the chunk to the database
                chunk.to_sql(table_name, con=engine, if_exists='append', index=False)
                print(f"Successfully uploaded chunk with {len(chunk)} rows.")
                
            print("Data import complete.")
        except Exception as e:
            print(f"An error occurred: {e}")

def clean_products():
    # Connect to the database using psycopg2
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    try:
        # Get the total number of rows in stock_29
        cur.execute("SELECT COUNT(*) FROM products_29;")
        total_rows = cur.fetchone()[0]
        
        offset = 0
        while offset < total_rows:
            # Define the query with OFFSET and LIMIT
            paginated_query = f"""
            WITH pc AS(
                SELECT product_categories.id, product_categories_29.id AS old_id
                FROM product_categories
                JOIN product_categories_29 ON product_categories.name = product_categories_29.name
            ),
            source AS (
                SELECT name, purchase_price, selling_price, pc.id AS category_id, 3 AS shop_id 
                FROM products_29
                JOIN pc ON pc.old_id = products_29.category_id
            )
            INSERT INTO products(name, purchase_price, selling_price, category_id, shop_id)
            SELECT * FROM source
            LIMIT {chunk_size} OFFSET {offset}
            ON CONFLICT (name, shop_id) DO NOTHING
            """
            
            # Execute the query
            cur.execute(paginated_query)
            conn.commit()
            print(f"Successfully processed rows from {offset} to {offset + chunk_size - 1}.")
            
            # Move to the next chunk
            offset += chunk_size

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        cur.close()
        conn.close()

def clean_stock():
    # Connect to the database using psycopg2
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    try:
        # Get the total number of rows in stock_29
        cur.execute("SELECT COUNT(*) FROM stock_29;")
        total_rows = cur.fetchone()[0]
        
        offset = 0
        while offset < total_rows:
            # Define the query with OFFSET and LIMIT
            paginated_query = f"""
            WITH p AS (
                SELECT products.id, products.category_id, products_29.id AS old_id 
                FROM products
                JOIN products_29 ON products_29.name = products.name
            ),
            source AS(
                SELECT date AS stock_date, p.id AS product_id, name, p.category_id, purchase_price, selling_price, opening, additions, 3 AS shop_id 
                FROM stock_29
                JOIN p ON p.old_id = stock_29.product_id
            )
            INSERT INTO stock (stock_date, product_id, name, category_id, purchase_price, selling_price, opening, additions, shop_id)   
            SELECT * FROM source         
            LIMIT {chunk_size} OFFSET {offset}
            ON CONFLICT (stock_date, product_id, shop_id) DO NOTHING
            """
            
            # Execute the query
            cur.execute(paginated_query)
            conn.commit()
            print(f"Successfully processed rows from {offset} to {offset + chunk_size - 1}.")
            
            # Move to the next chunk
            offset += chunk_size

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        cur.close()
        conn.close()

def clean_customers():
    # Connect to the database using psycopg2
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    try:
        # Get the total number of rows in stock_29
        cur.execute("SELECT COUNT(*) FROM customers_29;")
        total_rows = cur.fetchone()[0]
        
        offset = 0
        while offset < total_rows:
            # Define the query with OFFSET and LIMIT
            paginated_query = f"""
            WITH source AS(
                SELECT name, phone, 3 AS shop_id 
                FROM customers_29
            )
            INSERT INTO customers (name, phone, shop_id)   
            SELECT * FROM source         
            LIMIT {chunk_size} OFFSET {offset}
            ON CONFLICT (phone, shop_id) DO NOTHING
            """
            
            # Execute the query
            cur.execute(paginated_query)
            conn.commit()
            print(f"Successfully processed rows from {offset} to {offset + chunk_size - 1}.")
            
            # Move to the next chunk
            offset += chunk_size

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        cur.close()
        conn.close()

def clean_bills():
    # Connect to the database using psycopg2
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    try:        
        # Get the total number of rows in stock_29
        cur.execute("SELECT COUNT(*) FROM bills_29;")
        total_rows = cur.fetchone()[0]
        
        offset = 0
        while offset < total_rows:
            # Define the query with OFFSET and LIMIT
            paginated_query = f"""
            WITH c AS (
                SELECT customers.id, customers_29.id AS old_id 
                FROM customers
                JOIN customers_29 ON customers_29.phone = customers.phone
            ),
            source AS(
                SELECT c.id AS customer_id, total, paid, 3 AS shop_id, created_at, 3 AS created_by
                FROM bills_29
                JOIN c ON c.old_id = bills_29.customer_id
            )
            INSERT INTO bills(customer_id, total, paid, shop_id, created_at, created_by)   
            SELECT * FROM source         
            LIMIT {chunk_size} OFFSET {offset}
            """
            
            # Execute the query
            cur.execute(paginated_query)
            conn.commit()
            print(f"Successfully processed rows from {offset} to {offset + chunk_size - 1}.")
            
            # Move to the next chunk
            offset += chunk_size

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        cur.close()
        conn.close()

def clean_bill_entries():
    # Connect to the database using psycopg2
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    try:        
        # Get the total number of rows in stock_29
        cur.execute("SELECT COUNT(*) FROM bill_entries_29;")
        total_rows = cur.fetchone()[0]
        
        offset = 0
        while offset < total_rows:
            # Define the query with OFFSET and LIMIT
            paginated_query = f"""
            WITH b AS (
                SELECT bills.id, bills_29.id AS old_id 
                FROM bills
                JOIN bills_29 ON bills_29.created_at = bills.created_at
            ),
            s AS(
                SELECT stock.id, stock_29.id AS old_id 
                FROM stock
                JOIN stock_29 ON stock_29.product_id = stock.product_id AND stock_29.date = stock.stock_date 
            ),
            source AS(
                SELECT b.id AS bill_id, s.id AS stock_id, item_name, price, qty, 3 AS shop_id, created_at, 3 AS created_by
                FROM bill_entries_29
                JOIN b ON b.old_id = bill_entries_29.bill_id
                JOIN s ON s.old_id = bill_entries_29.stock_id
            )
            INSERT INTO bill_entries(bill_id, stock_id, item_name, price, qty, shop_id, created_at, created_by) 
            SELECT * FROM source         
            LIMIT {chunk_size} OFFSET {offset}
            ON CONFLICT (bill_id, stock_id, created_by) DO UPDATE 
            SET qty = EXCLUDED.qty
            """
            
            # Execute the query
            cur.execute(paginated_query)
            conn.commit()
            print(f"Successfully processed rows from {offset} to {offset + chunk_size - 1}.")
            
            # Move to the next chunk
            offset += chunk_size

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        cur.close()
        conn.close()

def clean_payments():
    # Connect to the database using psycopg2
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    try:        
        #Truncate 
        cur.execute("TRUNCATE TABLE payments;")
        
        # Get the total number of rows in stock_29
        cur.execute("SELECT COUNT(*) FROM payments_29;")
        total_rows = cur.fetchone()[0]
        
        offset = 0
        while offset < total_rows:
            # Define the query with OFFSET and LIMIT
            paginated_query = f"""
            WITH b AS (
                SELECT bills.id, bills_29.id AS old_id 
                FROM bills
                JOIN bills_29 ON bills_29.created_at = bills.created_at
            ),
            source AS(
                SELECT b.id AS bill_id, amount, payment_mode_id, 3 AS shop_id, created_at, 3 AS created_by
                FROM payments_29
                JOIN b ON b.old_id = payments_29.bill_id
            )
            INSERT INTO payments(bill_id, amount, payment_mode_id, shop_id, created_at, created_by) 
            SELECT * FROM source         
            LIMIT {chunk_size} OFFSET {offset}
            """
            
            # Execute the query
            cur.execute(paginated_query)
            conn.commit()
            print(f"Successfully processed rows from {offset} to {offset + chunk_size - 1}.")
            
            # Move to the next chunk
            offset += chunk_size

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        cur.close()
        conn.close()

def clean_expenses():
    # Connect to the database using psycopg2
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    try:      
        #Truncate 
        cur.execute("TRUNCATE TABLE expenses;")
           
        # Get the total number of rows in stock_29
        cur.execute("SELECT COUNT(*) FROM expenses_29;")
        total_rows = cur.fetchone()[0]
        
        offset = 0
        while offset < total_rows:
            # Define the query with OFFSET and LIMIT
            paginated_query = f"""
            WITH source AS(
                SELECT date, name, amount, 3 AS shop_id, created_at, 3 AS created_by
                FROM expenses_29
            )
            INSERT INTO expenses(date, name, amount, shop_id, created_at, created_by) 
            SELECT * FROM source         
            LIMIT {chunk_size} OFFSET {offset}
            """
            
            # Execute the query
            cur.execute(paginated_query)
            conn.commit()
            print(f"Successfully processed rows from {offset} to {offset + chunk_size - 1}.")
            
            # Move to the next chunk
            offset += chunk_size

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        cur.close()
        conn.close()


#clean_expenses()
