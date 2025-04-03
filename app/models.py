from flask import session
import MySQLdb
import MySQLdb
import logging
from werkzeug.utils import secure_filename
from flask import session

class User:
    def __init__(self, id, username, password, email, image_path=None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.image_path = image_path

    @staticmethod
    def get_connection():
        """Get a connection to the database specified in the session."""
        selected_db = session.get('database')
        if not selected_db:
            raise Exception("Database not selected. User must log in.")
        return MySQLdb.connect(host="localhost", user="root", passwd="", db=selected_db)

    @staticmethod
    def get_user_by_username(username):
        """Fetch user by username."""
        db_connection = User.get_connection()
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user:
                return User(user[0], user[1], user[2], user[3], user[4])
            return None
        finally:
            db_connection.close()

    @staticmethod
    def register_user(username, email, hashed_password, location, business_type):
        """Register a user in the master database and the corresponding specific database."""
        database_mapping = {
            ('grocery', 'dhaka'): 'dbprobaho_gro_dha',
            ('restaurant', 'dhaka'): 'dbprobaho_res_dha',
            ('pharmacy', 'dhaka'): 'dbprobaho_phar_dha',
            ('grocery', 'barisal'): 'dbprobaho_gro_bar',
            ('restaurant', 'barisal'): 'dbprobaho_res_bar',
            ('pharmacy', 'barisal'): 'dbprobaho_phar_bar',
        }
        selected_database = database_mapping.get((business_type.lower(), location.lower()))

        if not selected_database:
            raise Exception("Invalid business type or location.")

        # Step 1: Insert user into the master database
        master_db = MySQLdb.connect(host="localhost", user="root", passwd="", db="dbprobaho_master")
        try:
            master_cursor = master_db.cursor()
            master_cursor.execute(
                "INSERT INTO users (userName, userPass, userEmail, userImage) VALUES (%s, %s, %s, NULL)",
                (username, hashed_password, email)
            )
            master_db.commit()
            user_id = master_cursor.lastrowid  # Get the newly generated user ID

            # Insert location and business type into the master DB
            master_cursor.execute(
                "INSERT INTO locations (locationName, userID) VALUES (%s, %s)", (location, user_id)
            )
            master_cursor.execute(
                "INSERT INTO businesstypes (businessTypeName, userID) VALUES (%s, %s)", (business_type, user_id)
            )
            master_db.commit()
        finally:
            master_db.close()

        # Step 2: Push user information to the selected database
        specific_db = MySQLdb.connect(host="localhost", user="root", passwd="", db=selected_database)
        try:
            specific_cursor = specific_db.cursor()
            specific_cursor.execute(
                "INSERT INTO users (userID, userName, userPass, userEmail, userImage) VALUES (%s, %s, %s, %s, NULL)",
                (user_id, username, hashed_password, email)
            )
            specific_cursor.execute(
                "INSERT INTO locations (locationName, userID) VALUES (%s, %s)", (location, user_id)
            )
            specific_cursor.execute(
                "INSERT INTO businesstypes (businessTypeName, userID) VALUES (%s, %s)", (business_type, user_id)
            )
            specific_db.commit()
        finally:
            specific_db.close()

        return user_id

    @staticmethod
    def update_image_path(user_id, image_path, username, password, business_type, location):
        """Update the user's image path in both the master and specific databases."""
        
        # Update in master database
        master_db = MySQLdb.connect(host="localhost", user="root", passwd="", db="dbprobaho_master")
        master_cursor = master_db.cursor()
        master_cursor.execute("UPDATE users SET userImage = %s WHERE userID = %s", (image_path, user_id))
        master_db.commit()

        # Get the specific database for the user based on business type and location
        database_mapping = {
            ('grocery', 'dhaka'): 'dbprobaho_gro_dha',
            ('restaurant', 'dhaka'): 'dbprobaho_res_dha',
            ('pharmacy', 'dhaka'): 'dbprobaho_phar_dha',
            ('grocery', 'barisal'): 'dbprobaho_gro_bar',
            ('restaurant', 'barisal'): 'dbprobaho_res_bar',
            ('pharmacy', 'barisal'): 'dbprobaho_phar_bar',
        }
        selected_db = database_mapping.get((business_type.lower(), location.lower()))
       
        if not selected_db:
            raise Exception("Invalid business type or location.")

        # Update in specific database
        specific_db = MySQLdb.connect(host="localhost", user="root", passwd="", db=selected_db)
        specific_cursor = specific_db.cursor()
        specific_cursor.execute("UPDATE users SET userImage = %s WHERE userID = %s", (image_path, user_id))
        specific_db.commit()

        # Close connections
        master_db.close()
        specific_db.close()

class Dashboard:
    @staticmethod
    def get_connection():
        """Get a connection to the database specified in the session."""
        selected_db = session.get('database')
        if not selected_db:
            raise Exception("Database not selected. User must log in.")
        return MySQLdb.connect(host="localhost", user="root", passwd="", db=selected_db)
    
    @staticmethod
    def fetch_card_data():
        """Fetch data for the dashboard cards."""
        db_connection = Dashboard.get_connection()
        user_id = session.get('user_id')
        try:
            cursor = db_connection.cursor()
            
            # Fetch sales total
            cursor.execute("SELECT COALESCE(SUM(totalAmount), 0) FROM bills WHERE userID = %s", (user_id,))
            sales = cursor.fetchone()[0]

            # Fetch total orders
            cursor.execute("SELECT COUNT(*) FROM bills WHERE userID = %s", (user_id,))
            orders = cursor.fetchone()[0]

            # Fetch total products
            cursor.execute("SELECT COUNT(*) FROM products WHERE userID = %s", (user_id,))
            products = cursor.fetchone()[0]

            # Fetch total staff
            cursor.execute("SELECT COUNT(*) FROM staff WHERE userID = %s", (user_id,))
            staff = cursor.fetchone()[0]

            return {
                'sales': sales,
                'orders': orders,
                'products': products,
                'staff': staff
            }
        finally:
            db_connection.close()
    @staticmethod
    def fetch_monthly_sales_data():
        """Fetch monthly sales data for the chart."""
        db_connection = Dashboard.get_connection()
        user_id = session.get('user_id')
        month_mapping = {
            "01": "January", "02": "February", "03": "March", "04": "April",
            "05": "May", "06": "June", "07": "July", "08": "August",
            "09": "September", "10": "October", "11": "November", "12": "December"
        }
        try:
            cursor = db_connection.cursor()
            query = """
                SELECT 
                    DATE_FORMAT(billDate, '%%m') AS month, -- Numeric month
                    SUM(totalAmount) AS total
                FROM bills
                WHERE userID = %s
                GROUP BY MONTH(billDate)
                ORDER BY MONTH(billDate)
            """
            cursor.execute(query, (user_id,))
            data = cursor.fetchall()
            # Map numeric month to full month names
            return [{'month': month_mapping[row[0]], 'total': float(row[1])} for row in data]
        finally:
            db_connection.close()
            
    @staticmethod
    def fetch_demanding_products_data():
        """Fetch data for the most demanding products."""
        db_connection = Dashboard.get_connection()
        user_id = session.get('user_id')  # Ensure the user ID is stored in the session
        try:
            cursor = db_connection.cursor()
            query = """
                SELECT 
                    products.productName, 
                    SUM(bill_items.quantity) AS demand
                FROM bill_items
                JOIN products ON bill_items.productID = products.productID
                WHERE products.userID = %s
                GROUP BY products.productName
                ORDER BY demand DESC
                LIMIT 5
            """
            cursor.execute(query, (user_id,))
            data = cursor.fetchall()
            # Convert fetched data into a list of dictionaries
            return [{'product': row[0], 'demand': int(row[1])} for row in data]
        finally:
            db_connection.close()

class Category:
    @staticmethod
    def get_connection():
        """Get a connection to the database specified in the session."""
        selected_db = session.get('database')
        if not selected_db:
            raise Exception("Database not selected. User must log in.")
        return MySQLdb.connect(host="localhost", user="root", passwd="", db=selected_db)

    @staticmethod
    def get_all_categories():
        """Fetch all categories from the database."""
        db_connection = Category.get_connection()
        user_id = session.get('user_id')
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM category WHERE userID = %s", (user_id,))
            categories = cursor.fetchall()
            return categories
        finally:
            db_connection.close()

    @staticmethod
    def add_category(cat_name):
        """Add a new category to the database."""
        db_connection = Category.get_connection()
        user_id = session.get('user_id')
        try:
            cursor = db_connection.cursor()
            cursor.execute("INSERT INTO category (catName,userID) VALUES (%s,%s)", (cat_name,user_id,))
            db_connection.commit()
        finally:
            db_connection.close()

    @staticmethod
    def update_category(cat_id, cat_name):
        """Update an existing category."""
        db_connection = Category.get_connection()
        try:
            cursor = db_connection.cursor()
            cursor.execute("UPDATE category SET catName = %s WHERE catID = %s", (cat_name, cat_id))
            db_connection.commit()
        finally:
            db_connection.close()

    @staticmethod
    def delete_category(cat_id):
        """Delete a category from the database."""
        db_connection = Category.get_connection()
        try:
            cursor = db_connection.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("DELETE FROM category WHERE catID = %s", (cat_id,))
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            db_connection.commit()
        finally:
            db_connection.close()

    @staticmethod
    def search_categories(search_term):
        """Search categories by name based on the search term."""
        db_connection = Category.get_connection()
        user_id = session.get('user_id')
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM category WHERE catName LIKE %s AND userID = %s", ('%' + search_term + '%',user_id,))
            categories = cursor.fetchall()
            return categories
        finally:
            db_connection.close()


class Product:
    @staticmethod
    def get_connection():
        """Get a connection to the database specified in the session."""
        selected_db = session.get('database')
        if not selected_db:
            raise Exception("Database not selected. User must log in.")
        return MySQLdb.connect(host="localhost", user="root", passwd="", db=selected_db)

    @staticmethod
    def get_all_products():
        """Fetch all products from the database."""
        db_connection = Product.get_connection()
        user_id = session.get('user_id')
        try:
            cursor = db_connection.cursor()
            cursor.execute("""
                SELECT products.productID, products.productName, products.productPrice, 
                    products.productStock, products.productDescription, products.barcode_id, 
                    products.expiryDate, category.catName
                FROM products
                JOIN category ON products.catID = category.catID
                           WHERE products.userID=%s
            """,(user_id,))
            products = cursor.fetchall()
            return products
        finally:
            db_connection.close()

    @staticmethod
    def add_product(prod_name, prod_price, prod_stock, prod_description, prod_category_id, barcode_value, expiry_date, image_path=None):
        """Add a new product to the database."""
        db_connection = Product.get_connection()
        user_id = session.get('user_id')
        try:
            cursor = db_connection.cursor()
            cursor.execute("""
                INSERT INTO products (productName, productPrice, productStock, productDescription, catID, barcode_id, expiryDate, productImage,userID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (prod_name, prod_price, prod_stock, prod_description, prod_category_id, barcode_value, expiry_date, image_path,user_id))
            db_connection.commit()
        finally:
            db_connection.close()

    @staticmethod
    def update_product(prod_id, prod_name, prod_price, prod_stock, prod_description, prod_category_id, barcode_value, expiry_date, image_path=None):
        """Update an existing product in the database."""
        db_connection = Product.get_connection()
        user_id = session.get('user_id')
        try:
            cursor = db_connection.cursor()
            cursor.execute("""
                UPDATE products 
                SET productName=%s, productPrice=%s, productStock=%s, productDescription=%s, 
                    catID=%s, barcode_id=%s, expiryDate=%s, productImage=%s
                WHERE productID=%s
            """, (prod_name, prod_price, prod_stock, prod_description, prod_category_id, barcode_value, expiry_date, image_path, prod_id))
            db_connection.commit()
        finally:
            db_connection.close()
    @staticmethod
    def get_product_by_id(prod_id):
        """Fetch a product from the database by its ID."""
        db_connection = Product.get_connection()
        try:
            cursor = db_connection.cursor()
            cursor.execute("""
                SELECT productID, productName, productPrice, productStock, productDescription, 
                    catID, productImage, barcode_id, expiryDate, userID
                FROM products
                WHERE productID = %s
            """, (prod_id,))
            product = cursor.fetchone()
            return product
        finally:
            db_connection.close()
            
    @staticmethod
    def delete_product(prod_id):
        """Delete a product from the database."""
        db_connection = Product.get_connection()
        try:
            cursor = db_connection.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("DELETE FROM products WHERE productID = %s", (prod_id,))
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            db_connection.commit()
        finally:
            db_connection.close()

    @staticmethod
    def search_products(search_term, category_filter=None):
        """Search products based on a search term (and optional category filter)."""
        db_connection = Product.get_connection()
        user_id = session.get('user_id')
        try:
            if category_filter:
                cursor = db_connection.cursor()
                cursor.execute("""
                    SELECT products.productID, products.productName, products.productPrice, 
                           products.productStock, products.productDescription, products.barcode_id, products.expiryDate, category.catName
                    FROM products
                    JOIN category ON products.catID = category.catID
                    WHERE (products.productName LIKE %s OR products.productDescription LIKE %s)
                    AND category.catID = %s AND products.userID=%s
                """, ('%' + search_term + '%', '%' + search_term + '%', category_filter,user_id))
            elif search_term:
                cursor = db_connection.cursor()
                cursor.execute("""
                    SELECT products.productID, products.productName, products.productPrice, 
                           products.productStock, products.productDescription, products.barcode_id, products.expiryDate, category.catName
                    FROM products
                    JOIN category ON products.catID = category.catID
                    WHERE products.productName LIKE %s OR products.barcode_id LIKE %s AND products.userID=%s
                """, ('%' + search_term + '%', '%' + search_term + '%',user_id))
            else:
                Product.get_all_products();
            
            products = cursor.fetchall()
            return products
        finally:
            db_connection.close()

    
    @staticmethod
    def search_products_by_expiry_date(search_term=None, category_filter=None, expiry_date=None):
        """Search products expiring before a given date (with optional name and category filters)."""
        db_connection = Product.get_connection()
        user_id = session.get('user_id')
        try:
            query = """
                SELECT products.productID, products.productName, products.productPrice, 
                    products.productStock, products.productDescription, products.barcode_id, 
                    products.expiryDate, category.catName
                FROM products
                JOIN category ON products.catID = category.catID
                WHERE products.userID = %s
            """
            params = [user_id]

            if search_term:
                query += " AND (products.productName LIKE %s OR products.barcode_id LIKE %s)"
                params.extend(['%' + search_term + '%', '%' + search_term + '%'])
            if expiry_date:
                query += " AND DATE(products.expiryDate) < %s"
                params.append(expiry_date)

            cursor = db_connection.cursor()
            cursor.execute(query, tuple(params))
            products = cursor.fetchall()
            return products
        finally:
            db_connection.close()


class Bill:
    @staticmethod
    def get_connection():
        """Get a connection to the database specified in the session."""
        selected_db = session.get('database')
        if not selected_db:
            raise Exception("Database not selected. User must log in.")
        return MySQLdb.connect(host="localhost", user="root", passwd="", db=selected_db)

    @staticmethod
    def create_bill(bill_data):
        """Create a new bill in the database."""
        db_connection = Bill.get_connection()
        try:
            cursor = db_connection.cursor()
            cursor.execute("""
                INSERT INTO bills (userID, totalAmount, customerName, customerContact, customerAddress, customerEmail, paymentMethod)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (bill_data['user_id'], bill_data['total_amount'], bill_data['customer_name'],
                  bill_data['customer_mobile'], bill_data['customer_address'],
                  bill_data['customer_email'], bill_data['payment_method']))
            db_connection.commit()
            return cursor.lastrowid  # Return the bill ID
        finally:
            db_connection.close()

    @staticmethod
    def add_bill_items(bill_id, items):
        """Add bill items to the database."""
        db_connection = Bill.get_connection()
        try:
            cursor = db_connection.cursor()
            for item in items:
                cursor.execute("""
                    INSERT INTO bill_items (billID, productID, quantity, pricePerUnit, totalPrice)
                    VALUES (%s, %s, %s, %s, %s)
                """, (bill_id, item['product_id'], item['quantity'], item['price'],
                      item['quantity'] * item['price']))
                # Reduce the product quantity in the database
                cursor.execute("""
                    UPDATE products
                    SET productStock = productStock - %s
                    WHERE productID = %s AND productStock >= %s
                """, (item['quantity'], item['product_id'], item['quantity']))
            db_connection.commit()
        finally:
            db_connection.close()

class Pos:
    @staticmethod
    def get_connection():
        """Get a connection to the database specified in the session."""
        selected_db = session.get('database')
        if not selected_db:
            raise Exception("Database not selected. User must log in.")
        return MySQLdb.connect(host="localhost", user="root", passwd="", db=selected_db)


    @staticmethod
    def add_to_cart(product_id, quantity=1):
        selected_items = session.get('selected_items', [])
        product = Product.get_product_by_id(product_id)
        if product and product[3] >= quantity:  # Assuming product stock is at index 3
            # Add or update cart item
            existing_item = next((item for item in selected_items if item['product_id'] == product_id), None)
            if existing_item:
                existing_item['quantity'] += quantity
            else:
                selected_items.append({
                    'product_id': product_id,
                    'product_name': product[1],
                    'price': product[2],
                    'quantity': quantity
                })
            session['selected_items'] = selected_items
        else:
            raise Exception("Not enough stock available.")


    @staticmethod
    def remove_from_cart(product_id):
        """Remove a product from the cart (session)."""
        selected_items = session.get('selected_items', [])
        selected_items = [item for item in selected_items if item['product_id'] != product_id]
        session['selected_items'] = selected_items

    @staticmethod
    def update_quantity_in_cart(product_id, quantity):
        selected_items = session.get('selected_items', [])
        product_found = False
        for item in selected_items:
            if item['product_id'] == product_id:
                item['quantity'] = quantity
                product_found = True
                break
        if not product_found:
            raise Exception("Product not found in cart.")
        session['selected_items'] = selected_items


    @staticmethod
    def get_cart_items():
        """Retrieve the current cart items from the session."""
        return session.get('selected_items', [])
    
    @staticmethod
    def prepare_bill():
        """Prepare the bill by calculating the total amount and gathering items."""
        # Get selected items from the session
        selected_items = session.get('selected_items', [])
        if not selected_items:
            raise ValueError("No items in the cart to prepare a bill.")

        # Validate selected items and calculate total amount
        total_amount = 0
        valid_items = []
        for item in selected_items:
            # Retrieve price and quantity with validation
            price = item.get('price')
            quantity = item.get('quantity')

            # Validate price and quantity
            if price is None or quantity is None:
                logging.error(f"Invalid item detected: {item}")  # Log error for debugging
                raise ValueError(f"Item price or quantity is missing for product {item.get('product_id')}")
            
            if not isinstance(price, (int, float)) or not isinstance(quantity, int):
                logging.error(f"Invalid types for item: {item}")  # Log error for debugging
                raise ValueError(f"Invalid price or quantity for product {item.get('product_id')}: {item}")

            # Add validated item to valid_items and update total amount
            valid_items.append(item)
            total_amount += price * quantity

        # Get customer details from the session
        customer_info = session.get('customer_info', {})
        if not customer_info:
            raise ValueError("Customer information is missing.")

        # Build the bill data
        bill_data = {
            'user_id': session.get('user_id', None),  # Assuming user_id is available in the session
            'customer_name': customer_info.get('name', 'N/A'),
            'customer_contact': customer_info.get('mobile', 'N/A'),
            'payment_method': "Cash",  # Could be dynamic based on user input
            'total_amount': total_amount,
            'items': valid_items,
        }

        return bill_data

    @staticmethod
    def clear_cart():
        """Clear all items from the cart."""
        session['selected_items'] = []

    @staticmethod
    def get_cart_summary():
        selected_items = session.get('selected_items', [])
        total_price = sum(item['price'] * item['quantity'] for item in selected_items)
        return selected_items, total_price



class Staff:
    def __init__(self, staff_id, first_name, last_name, position, email, phone, hire_date,salary,userid):
        self.staff_id = staff_id
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.email = email
        self.phone = phone
        self.hire_date=hire_date
        self.salary=salary
        self.userid=userid

    @staticmethod
    def get_connection():
        """Establish a connection to the selected database."""
        selected_db = session.get('database')
        if not selected_db:
            raise Exception("Database not selected. Please log in.")
        return MySQLdb.connect(host="localhost", user="root", passwd="", db=selected_db)

    @staticmethod
    def get_staff_by_username(username):
        """Retrieve a staff member by their username."""
        db_connection = Staff.get_connection()
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM staff WHERE username = %s", (username,))
            staff = cursor.fetchone()
            if staff:
                return Staff(*staff)  # Unpack the fetched staff tuple into the Staff object
            return None
        finally:
            db_connection.close()

    @staticmethod
    def add_staff(first_name, last_name, email, position, phone_number, hire_date, salary, user_id):
        """Add a new staff member to the database."""
        db_connection = Staff.get_connection()
        try:
            cursor = db_connection.cursor()
            cursor.execute(
                """
                INSERT INTO staff (FirstName, LastName, Email, Position, PhoneNumber, HireDate, Salary, userID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (first_name, last_name, email, position, phone_number, hire_date, salary, user_id)
            )
            db_connection.commit()  # Commit transaction to save changes
        except Exception as e:
            print(f"Error adding staff: {e}")  # Log the error
            db_connection.rollback()  # Rollback transaction on error
            raise
        finally:
            db_connection.close()

    @staticmethod
    def update_staff_info(staff_id, first_name, last_name, position, email, phone_number, salary):
        """Update the details of a staff member."""
        db_connection = Staff.get_connection()
        try:
            cursor = db_connection.cursor()
            cursor.execute(
                """
                UPDATE staff 
                SET FirstName = %s, LastName = %s, Position = %s, Email = %s, 
                    PhoneNumber = %s, Salary = %s
                WHERE StaffID = %s
                """,
                (first_name, last_name, position, email, phone_number, salary, staff_id)
            )
            db_connection.commit()
        except MySQLdb.Error as e:
            db_connection.rollback()
            raise Exception(f"Error updating staff info: {e}")
        finally:
            db_connection.close()

    @staticmethod
    def delete_staff(staff_id):
        """Delete a staff member by their ID."""
        db_connection = Staff.get_connection()
        try:
            cursor = db_connection.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")  # Disable foreign key checks
            cursor.execute("DELETE FROM staff WHERE staffID = %s", (staff_id,))
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")  # Re-enable foreign key checks
            db_connection.commit()
        except MySQLdb.Error as e:
            db_connection.rollback()
            raise Exception(f"Error deleting staff: {e}")
        finally:
            db_connection.close()

    @staticmethod
    def get_all_staff():
        """Retrieve all staff members from the database."""
        db_connection = Staff.get_connection()
        try:
            cursor = db_connection.cursor()
            cursor.execute(
                """
                SELECT StaffID, FirstName, LastName, position, email, PhoneNumber, salary
                FROM staff
                ORDER BY HireDate DESC
                """
            )
            return cursor.fetchall()  # Fetch all rows
        finally:
            db_connection.close()
            
    @staticmethod
    def get_staff_by_id(staff_id):
        """Retrieve a staff member by their staff ID."""
        db_connection = Staff.get_connection()
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM staff WHERE StaffID = %s", (staff_id,))
            staff = cursor.fetchone()
            if staff:
                return Staff(*staff)  # Unpack the fetched staff tuple into the Staff object
            return None
        finally:
            db_connection.close()