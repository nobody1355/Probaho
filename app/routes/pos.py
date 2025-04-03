from flask import Blueprint, render_template, request, jsonify, session
import logging
from app.models import Product, Bill, Pos

# Initialize the Blueprint for POS
pos = Blueprint('pos', __name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Route to display POS page with products, and customer form
@pos.route('/pos', methods=['GET', 'POST'])
def point_of_sale():
    try:
        # Get the list of products
        products_list = Product.get_all_products()

        # Initialize or get cart (selected items) from the session
        selected_items = Pos.get_cart_items()

        if request.method == 'POST':
            # Handle product search and customer info submission
            search_query = request.form.get('search_query', '')
            customer_name = request.form.get('customer_name', '')
            customer_mobile = request.form.get('customer_mobile', '')
            customer_address = request.form.get('customer_address', '')
            customer_email = request.form.get('customer_email', '')

            # Update the session with the customer information
            session['customer_info'] = {
                'name': customer_name,
                'mobile': customer_mobile,
                'address': customer_address,
                'email': customer_email
            }

            # Filter products based on search query
            if search_query:
                products_list = Product.search_products(search_query)

        return render_template('pos/pos.html', products=products_list, selected_items=selected_items)

    except Exception as e:
        logging.error(f"Error in point_of_sale: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Route to handle product search via barcode or name
@pos.route('/pos/search', methods=['GET'])
def search_products():
    try:
        search_term = request.args.get('searchTerm', '')
        category_id = request.args.get('categoryId', '')
        products = Product.search_products(search_term, category_id)

        return jsonify({'products': products})
    except Exception as e:
        logging.error(f"Error in search_products: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400


# Route to add or remove products from the cart (selected items)
@pos.route('/pos/cart', methods=['POST'])
def update_cart():
    try:
        product_id = request.form.get('product_id')
        action = request.form.get('action')  # 'add', 'remove', or 'update_quantity'
        quantity = int(request.form.get('quantity', 1))  # Default to 1 if no quantity specified

        # Add or remove products based on action
        if action == 'add':
            Pos.add_to_cart(product_id, quantity)
        elif action == 'remove':
            Pos.remove_from_cart(product_id)
        elif action == 'update_quantity':
            Pos.update_quantity_in_cart(product_id, quantity)

        # Return updated cart
        selected_items = Pos.get_cart_items()
        return jsonify({"selected_items": selected_items})

    except Exception as e:
        logging.error(f"Error in update_cart: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400


# Route to prepare the bill
@pos.route('/prepareBill', methods=['POST'])
def prepare_bill():
    try:
        logging.debug(f"Request Headers: {request.headers}")
        logging.debug(f"Request Data: {request.data}")

        bill_data = request.json  # Parse JSON payload
        if not bill_data:
            raise ValueError("Invalid or empty JSON payload received.")

        # Extract and validate cart items
        cart_items = bill_data.get('cart_items', [])
        if not cart_items:
            raise ValueError("Cart is empty.")

        for item in cart_items:
            if item.get('price') is None or item.get('quantity') is None:
                raise ValueError(f"Missing price or quantity in item: {item}")
            if not isinstance(item['price'], (int, float)) or not isinstance(item['quantity'], int):
                raise ValueError(f"Invalid data type in item: {item}")

        # Prepare bill using the validated data
        total_amount = sum(item['price'] * item['quantity'] for item in cart_items)
        customer_name = bill_data.get('customer_name', 'N/A')
        customer_mobile = bill_data.get('customer_mobile', 'N/A')
        customer_address = bill_data.get('customer_address', 'N/A')
        customer_email = bill_data.get('customer_email', 'N/A')

        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'status': 'error', 'message': 'User not logged in.'}), 401

        # Save bill to the database
        bill_id = Bill.create_bill({
            'user_id': user_id,
            'total_amount': total_amount,
            'customer_name': customer_name,
            'customer_mobile': customer_mobile,
            'customer_address': customer_address,
            'customer_email': customer_email,
            'payment_method': "Cash",
        })
        Bill.add_bill_items(bill_id, cart_items)

        # Clear the cart after successful transaction
        Pos.clear_cart()
        return jsonify({'status': 'success', 'bill_id': bill_id}), 200

    except ValueError as ve:
        logging.error(f"Validation Error in prepare_bill: {ve}")
        return jsonify({'status': 'error', 'message': str(ve)}), 400
    except Exception as e:
        logging.error(f"Unexpected Error in prepare_bill: {e}")
        return jsonify({'status': 'error', 'message': 'An unexpected error occurred.'}), 500


# Route to clear the cart (reset cart)
@pos.route('/pos/clear_cart', methods=['POST'])
def clear_cart():
    try:
        Pos.clear_cart()
        return jsonify({"selected_items": []})
    except Exception as e:
        logging.error(f"Error in clear_cart: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400
