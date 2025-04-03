from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Category

category = Blueprint('category', __name__)

@category.route('/categories')
def show_categories():
    categories = Category.get_all_categories()  # Fetch categories from the database
    return render_template('category/category.html', categories=categories)


@category.route('/category/add', methods=['POST'])
def add_category():
    cat_name = request.form['catName']
    Category.add_category(cat_name)  # Add the new category to the database
    return redirect(url_for('category.show_categories'))


@category.route('/category/edit', methods=['POST'])
def edit_category():
    cat_id = request.form['catID']
    cat_name = request.form['catName']
    Category.update_category(cat_id, cat_name)  # Update the category in the database
    return redirect(url_for('category.show_categories'))


@category.route('/category/delete/<int:cat_id>', methods=['POST'])
def delete_category(cat_id):
    Category.delete_category(cat_id)  # Delete the category from the database
    return redirect(url_for('category.show_categories'))


@category.route('/category/search', methods=['GET'])
def search_category():
    search_term = request.args.get('searchTerm', '')  # Get search term from the query string
    if search_term:
        categories = Category.search_categories(search_term)  # Filter categories by the search term
    else:
        categories = Category.get_all_categories()  # Fetch all categories if no search term
    return render_template('category/category.html', categories=categories)
