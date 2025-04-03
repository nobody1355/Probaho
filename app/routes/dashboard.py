from flask import Blueprint, render_template, session
from flask import jsonify
from app.models import Dashboard

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
def show_dashboard():
    """Render the dashboard with card data."""
    try:
        # Fetch card data from the database
        card_data = Dashboard.fetch_card_data()

        # Render the template with the card data
        return render_template('main/dashboard.html', card_data=card_data)
    except Exception as e:
        # Log error and display an error page if needed
        return render_template('error.html', message=str(e))
    
@dashboard.route('/dashboard/chart/sales')
def fetch_monthly_sales():
    """API endpoint to fetch monthly sales data."""
    try:
        data = Dashboard.fetch_monthly_sales_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard.route('/dashboard/chart/demanding-products')
def fetch_demanding_products():
    """API endpoint to fetch most demanding products data."""
    try:
        data = Dashboard.fetch_demanding_products_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500