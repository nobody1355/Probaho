from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Staff

# Initialize the Blueprint for staff
staff = Blueprint('staff', __name__)

# Route to display all staff members
@staff.route('/staff')
def show_staff():
    staff_members = Staff.get_all_staff()  # Fetch all staff members from the database
    return render_template('staff/staff.html', staff_members=staff_members)

# Route to add a new staff member
@staff.route('/add_staff', methods=['POST'])
def add_staff():
    try:
        # Retrieve form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        position = request.form.get('position', None)  # Optional
        phone_number = request.form.get('phone_number', None)  # Optional
        hire_date = request.form['hire_date']
        salary = request.form['salary']
        user_id = request.form['user_id']

        # Add staff to the database
        Staff.add_staff(first_name, last_name, email, position, phone_number, hire_date, salary, user_id)
        flash("Staff added successfully!", "success")
    except Exception as e:
        flash(f"Error adding staff: {e}", "danger")

    # Fetch updated staff list and render page
    staff_members = Staff.get_all_staff()
    return render_template('staff/staff.html', staff_members=staff_members)


# Route to edit an existing staff member
@staff.route('/staff/edit', methods=['POST'])
def edit_staff():
    staff_id = request.form['staff_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    position = request.form['position']
    email = request.form['email']
    phone_number = request.form['phone_number']
    salary = request.form['salary']

    try:
        Staff.update_staff_info(staff_id, first_name, last_name, position, email, phone_number, salary)
        flash("Staff information updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating staff: {e}", "danger")

    return redirect(url_for('staff.show_staff'))  # Replace with the route to show the staff list


# Route to delete a staff member
@staff.route('/staff/delete/<int:staff_id>', methods=['POST', 'GET'])
def delete_staff(staff_id):
    try:
        Staff.delete_staff(staff_id)  # Delete the staff member from the database
        flash('Staff member deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting staff member: {e}', 'danger')

    return redirect(url_for('staff.show_staff'))
