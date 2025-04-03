# app/routes/auth.py
import secrets
import shutil
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_mail import Message
from app import mail
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User
import MySQLdb

auth = Blueprint('auth', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_database_for_user(business_type, location):
  
    database_mapping = {
        ('grocery', 'dhaka'): 'dbprobaho_gro_dha',
        ('restaurant', 'dhaka'): 'dbprobaho_res_dha',
        ('pharmacy', 'dhaka'): 'dbprobaho_phar_dha',
        ('grocery', 'barisal'): 'dbprobaho_gro_bar',
        ('restaurant', 'barisal'): 'dbprobaho_res_bar',
        ('pharmacy', 'barisal'): 'dbprobaho_phar_bar',
    }
    return database_mapping.get((business_type.lower(), location.lower()))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the master database to fetch user information
        master_db = MySQLdb.connect(host="localhost", user="root", passwd="", db="dbprobaho_master")
        cur = master_db.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if user and check_password_hash(user[2], password):  # user[2] is the hashed password
            # Fetch user's business type and location
            cur.execute(""" 
                SELECT b.businessTypeName, l.locationName 
                FROM businesstypes b 
                JOIN locations l ON b.userID = l.userID 
                WHERE b.userID = %s
            """, (user[0],))
            user_data = cur.fetchone()
            master_db.close()

            if user_data:
                business_type, location = user_data
                selected_database = get_database_for_user(business_type, location)

                if selected_database:
                    # Save selected database in the session
                    session['database'] = selected_database
                    session['user_id'] = user[0]
                    session['username'] = user[1]
                    flash('Login successful!', 'success')
                    return redirect(url_for('dashboard.show_dashboard'))
                else:
                    flash('Invalid business type or location.', 'danger')
            else:
                flash('Unable to fetch user data.', 'danger')
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('auth/login.html')


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        user_email = request.form['email']

        # Check if the email exists in the database
        master_db = MySQLdb.connect(host="localhost", user="root", passwd="", db="dbprobaho_master")
        cur = master_db.cursor()
        cur.execute("SELECT * FROM users WHERE userEmail = %s", (user_email,))
        user = cur.fetchone()
        
        if user:
            # Generate a password reset token
            reset_token = secrets.token_urlsafe(16)

            # Save the token to the user's record in the database
            cur.execute("UPDATE users SET reset_token = %s WHERE userEmail = %s", (reset_token, user_email))
            master_db.commit()

            # Send the reset email
            reset_url = url_for('auth.reset_password', token=reset_token, _external=True)
            send_reset_email(user_email, reset_url)

            flash('A password reset link has been sent to your email.', 'success')
        else:
            flash('Email not found.', 'danger')

        master_db.close()

    return render_template('auth/forgot_password.html')


def send_reset_email(user_email, reset_url):
    """
    Sends a password reset email to the user.
    """
    msg = Message(
        subject="Probaho - Password Reset Request",
        recipients=[user_email],  # Recipient's email address
        body=f"Hello,\n\nTo reset your password, please click on the following link:\n{reset_url}\n\nIf you did not request a password reset, please ignore this email.\n\nBest Regards,\nProbaho Team"
    )
    try:
        mail.send(msg)
        print("Password reset email sent successfully!")
    except Exception as e:
        print(f"Error sending reset email: {e}")


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Verify the token exists and is valid
    master_db = MySQLdb.connect(host="localhost", user="root", passwd="", db="dbprobaho_master")
    cur = master_db.cursor()
    cur.execute("SELECT * FROM users WHERE reset_token = %s", (token,))
    user = cur.fetchone()

    if not user:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.reset_password', token=token))

        # Hash the new password before saving it
        hashed_password = generate_password_hash(new_password)

        # Update the user's password and reset the token
        cur.execute("UPDATE users SET userPass = %s, reset_token = NULL WHERE reset_token = %s", (hashed_password, token))
        master_db.commit()
        master_db.close()

        flash('Your password has been reset successfully!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', token=token)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        user_email = request.form['email']
        password = request.form['password']
        location = request.form['location']
        business_type = request.form['business_type']
        hashed_password = generate_password_hash(password)

        # Generate a verification token
        verification_token = secrets.token_urlsafe(16)

        file = request.files.get('user_image')
        image_path = 'static/images/userimage/default_user.png'  # Default image path

        # Determine the database based on business type and location
        selected_db = get_database_for_user(business_type, location)
        if not selected_db:
            flash('Invalid business type or location.', 'danger')
            return render_template('auth/register.html')

        # Register the user and get the user ID
        user_id = User.register_user(username, user_email, hashed_password, location, business_type)

        # Handle file upload if present
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        if file and allowed_file(file.filename):
            original_extension = file.filename.rsplit('.', 1)[1].lower()
            filename = f"user_{user_id}.{original_extension}"
            image_path = os.path.join(upload_folder, filename)
            file.save(image_path)
        
        # After the user is registered and image path is set, update the image path in the selected database
        User.update_image_path(user_id, image_path, username, password, business_type, location)

        # Save the verification token in the master database
        master_db = MySQLdb.connect(host="localhost", user="root", passwd="", db="dbprobaho_master")
        cur = master_db.cursor()
        cur.execute("UPDATE users SET verification_token = %s WHERE userEmail = %s", (verification_token, user_email))
        master_db.commit()
        master_db.close()

        # Send verification email
        #send_verification_email(user_email, verification_token)

        # Send registration email
        send_registration_email(user_email, verification_token)
        
        flash('Registration successful! Please verify your email to complete registration.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

# def send_verification_email(user_email, verification_token):
#     verify_url = url_for('auth.verify_email', token=verification_token, _external=True)

#     msg = Message("Please Verify Your Email",
#                   recipients=[user_email])  # recipient is the user's email
#     msg.body = f"""
#     Thank you for registering with Probaho!

#     Please click the link below to verify your email address:
#     {verify_url}

#     If you did not register, please ignore this email.

#     Best regards,
#     Team Probaho
#     """

    try:
        mail.send(msg)
        print("Verification email sent successfully!")
    except Exception as e:
        print(f"Error sending verification email: {e}")


@auth.route('/verify-email/<token>')
def verify_email(token):
    # Connect to the master database to verify the token
    master_db = MySQLdb.connect(host="localhost", user="root", passwd="", db="dbprobaho_master")
    cur = master_db.cursor()
    
    # Query the database to find a user with the given token
    cur.execute("SELECT * FROM users WHERE verification_token = %s", (token,))
    user = cur.fetchone()
    
    if user:
        # Token is valid, mark the user's email as verified
        cur.execute("UPDATE users SET verified = TRUE, verification_token = NULL WHERE verification_token = %s", (token,))
        master_db.commit()
        flash('Your email has been successfully verified! You can now log in.', 'success')
    else:
        # Token is invalid or expired
        flash('Invalid or expired verification link.', 'danger')
    
    master_db.close()
    return redirect(url_for('auth.login'))


def send_registration_email(user_email, verification_token):
    verification_url = url_for('auth.verify_email', token=verification_token, _external=True)
    
    msg = Message("Welcome to Probaho",
                  recipients=[user_email])
    
    msg.html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Probaho!</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            background-color: #f4f7fc;
            color: #333;
            margin: 0;
            padding: 0;
        }}
        .email-container {{
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            padding: 30px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .header h1 {{
            font-size: 24px;
            color: #5A2DFF;
            margin: 0;
        }}
        .content {{
            font-size: 16px;
            line-height: 1.6;
            color: #555;
            margin-bottom: 20px;
        }}
        .footer {{
            text-align: center;
            font-size: 14px;
            color: #888;
        }}
        .footer a {{
            color: #5A2DFF;
            text-decoration: none;
        }}
        .cta-btn {{
            display: inline-block;
            background-color: #5A2DFF;
            color: #fff;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            text-decoration: none;
            text-align: center;
            margin-top: 20px;
        }}
    </style>
</head>
<body>

    <div class="email-container">
        <div class="header">
            <h1>Welcome to Probaho!</h1>
        </div>
        
        <div class="content">
            <p>Thank you for registering with <strong>Probaho!</strong> We're excited to have you on board and can't wait to help you get started.</p>
        </div>

        <div class="footer">
            <p>Best regards,</p>
            <p><strong>Team Probaho</strong></p>
        </div>
    </div>

</body>
</html>
"""

    try:
        mail.send(msg)
        print("Verification email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
