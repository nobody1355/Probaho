#app/routes/main.py
#TIG Added lines 38-44

from flask import Blueprint, render_template, redirect, url_for, session, flash

# Define the 'main' blueprint
main = Blueprint('main', __name__)

# Route for the landing page (index.html)
@main.route('/')
def home():
    return render_template('index.html')  # Render the landing page

# Route for logging out
@main.route('/logout')
def logout():
    # Remove user data from session
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out', 'success')  # Flash a logout message
    return redirect(url_for('main.home'))  # Redirect to the landing page (index.html) after logout

@main.route('/features')
def features():
    return render_template('features.html')

@main.route('/documentation')
def documentation():
    return render_template('documentation.html')  # Render the documentation page

@main.route('/support')
def support():
    return render_template('support.html')  # Render the support page