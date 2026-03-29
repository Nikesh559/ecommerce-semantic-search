import psycopg2
from psycopg2 import Error
from . import product
import json

connection = psycopg2.connect(
            user="nsuthar",
            password="root123",
            host="127.0.0.1",
            port="5432",
            database="postgres"
        )
def insert_record(product: product.Product):
    try:
        cursor = connection.cursor()
        # SQL Query using placeholders
        insert_query = """ 
            INSERT INTO products (id, name, price, brand, description, category, attributes, s3_url) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
        """
        # 1. Create a cursor to perform database operations
        record_to_insert = (
            product.id,
            product.name,
            product.price,
            product.brand,
            product.description,
            product.category,
            json.dumps(product.attributes), 
            product.category +"/" + product.filename
        )

        cursor.execute(insert_query, record_to_insert)
        connection.commit()
        print(f"Product '{product.name}' inserted successfully!")

        # 4. CRITICAL: Commit the transaction
        # If you forget this, your data stays in limbo and never actually saves!
        connection.commit()
        print("Record inserted successfully!")

        return True

    except (Exception, Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
        if connection:
            connection.rollback() # Undo changes if something went wrong


def get_product_by_id(product_id):  
    try:
        # Using 'with' ensures the cursor closes automatically
        with connection.cursor() as cursor:
            # Match the order of your Product class: 
            # id, name, price, brand, description, category, attributes, filename
            select_query = """
                SELECT id, name, price, brand, description, category, attributes, s3_url 
                FROM products 
                WHERE id = %s
            """
            cursor.execute(select_query, (product_id,))
            result = cursor.fetchone()
            
            if result:
                return product.Product(*result)
            else:
                print(f"No product found with ID: {product_id}")
                return None

    except Exception as error:
        print(f"Error while querying PostgreSQL: {error}")
        return None