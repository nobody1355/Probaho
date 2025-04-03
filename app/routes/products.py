from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.models import Product, Category
import os

# Initialize the Blueprint for products
products = Blueprint('products', __name__)

# Route to display all products
@products.route('/products')
def show_products():
    products_list = Product.get_all_products()  # Fetch all products from the database
    categories = Category.get_all_categories()  # Fetch all categories for the dropdown
    return render_template('products/products.html', products=products_list, categories=categories)

# Route to add a new product
@products.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Retrieving the form data
        prod_name = request.form['prodName']
        prod_price = request.form['prodPrice']
        prod_stock = request.form['prodStock']
        prod_description = request.form['prodDescription']
        prod_category_id = request.form['catID']
        barcode_value = request.form['barcode_value']
        expiry_date = request.form['expiryDate'] 

        # Handle image file upload
        prod_image = request.files.get('prodImage')  # Retrieve the image from the form

        # Ensure the directory for product images exists
        image_dir = 'app/static/images/productImage'
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        
        # Handle the image upload and store it in the desired folder
        image_path = None  # Default to None in case no image is uploaded
        if prod_image:
            image_filename = secure_filename(prod_image.filename)
            image_path = os.path.join(image_dir, image_filename)  # Save image in the correct directory
            prod_image.save(image_path)

        # Add the product to the database
        try:
            Product.add_product(prod_name, prod_price, prod_stock, prod_description, prod_category_id, barcode_value, expiry_date, image_path)
            flash('Product added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding product: {e}', 'danger')
        
        return redirect(url_for('products.show_products'))

# Route to edit an existing product
@products.route('/products/edit/<int:prod_id>', methods=['GET', 'POST'])
def edit_product(prod_id):
    if request.method == 'GET':
        product = Product.get_product_by_id(prod_id)  # Fetch product from the database
        categories = Category.get_all_categories()  # Fetch all categories
        return render_template('products/edit_product.html', product=product, categories=categories)
    
    # If method is POST, then we will update the product
    prod_name = request.form['prodName']
    prod_price = request.form['prodPrice']
    prod_stock = request.form['prodStock']
    prod_description = request.form['prodDescription']
    prod_category_id = request.form['catID']
    barcode_value = request.form['barcode_value']
    expiry_date = request.form['expiryDate']
    
    # Handle image file upload if a new image is provided
    prod_image = request.files.get('prodImage')

    image_path = None  # Default to None
    if prod_image:
        image_filename = secure_filename(prod_image.filename)
        image_path = os.path.join('app/static/images/productImage', image_filename)  # Correct path
        prod_image.save(image_path)
    
    # Fetch the current image path from the database if no new image is uploaded
    current_product = Product.get_product_by_id(prod_id)
    if not image_path:
        image_path = current_product[6]  # Retain the existing image if no new image is provided

    # Update product information in the database
    try:
        Product.update_product(prod_id, prod_name, prod_price, prod_stock, prod_description, prod_category_id, barcode_value, expiry_date, image_path)
        flash('Product updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating product: {e}', 'danger')
    
    return redirect(url_for('products.show_products'))

# Route to delete a product
@products.route('/products/delete/<int:prod_id>', methods=['POST', 'GET'])
def delete_product(prod_id):
    try:
        Product.delete_product(prod_id)  # Delete the product from the database
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting product: {e}', 'danger')
    
    return redirect(url_for('products.show_products'))

# Route to search for products based on a search term and category
@products.route('/products/search', methods=['GET'])
def search_product():
    search_term = request.args.get('searchTerm', '')  # Get search term
    category_filter = request.args.get('searchCategory', '')  # Get category filter
    expiry_date = request.args.get('expiryDate', '')  # Get expiry date filter

    # Filter products based on search term, category, and expiry date (if applicable)
    if search_term and expiry_date:
        products_list = Product.search_products_by_expiry_date(search_term, expiry_date=expiry_date)
    elif expiry_date:
        products_list = Product.search_products_by_expiry_date(expiry_date=expiry_date)
    elif search_term:
        products_list = Product.search_products(search_term)
    else:
        products_list = Product.get_all_products()  # Fetch all products if no search/filter

    categories = Category.get_all_categories()  # Fetch categories
    return render_template('products/products.html', products=products_list, categories=categories)
