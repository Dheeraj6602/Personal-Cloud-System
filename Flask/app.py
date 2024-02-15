from flask import Flask, render_template, request, jsonify, session
from flask import flash, redirect, url_for
import sqlite3
import os
import boto3
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from botocore.exceptions import NoCredentialsError

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png'}

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY', '')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY', '')
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', '')
AWS_DOMAIN = os.environ.get('AWS_DOMAIN', '')


app = Flask(__name__)

app.secret_key = 'feathercoffeedistributorsightparticularessaysalvationbeeroutletethnic'

bcrypt = Bcrypt(app)

def connect_db():
    return sqlite3.connect('cloud_storage.db')

@app.route("/")
def load_index_page():
    return render_template("index.html", show_alert=False)

@app.route("/home")
def load_home_page():
    return render_template("home.html")

@app.route("/upload", methods=['GET', 'POST'])
def load_upload_page():
    if request.method == "POST":
        try:
            s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
            uploaded_file = request.form["file-name"]
            presigned_url = s3.generate_presigned_url(
                'put_object', Params={'Bucket': S3_BUCKET_NAME, 'Key': file_name})

            flash('Upload form loaded successfully', 'success')
        except:
            flash("AWS credentials not correct", "error")

    return render_template("upload.html")

@app.route("/account")
def load_account_page():
    user = session.get('user')
    print(user)
    return render_template("account.html", user=user)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('loginEmail')
    password = request.form.get('loginPassword')

    conn = sqlite3.connect('cloud_storage.db')
    c = conn.cursor()
    print("The details are: ", email, password)
    c.execute("SELECT * FROM Users WHERE email=? ", (email,))
    user = c.fetchone()
    print("user: ", user)

    session['user'] = {
        'user_id': user[0],
        'username': user[1],
        'email': user[2],
        'password': user[3],
        'phone': user[4],
        'address': user[5],
        'payment_info': user[6]
        # Add other user details as needed
    }

    if user and check_password(user[3], password):
        return render_template("home.html")  # User exists and password matches
    else:
        flash("Invalid email or password. Please try again.", "error")  # User does not exist or password is incorrect
        return render_template("index.html", show_alert_user_does_not_exist=True)
        #return load_index_page()

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Hash the password before storing it
    password_hash = hash_password(password)
    print("The details are: ", email, password, username)

    # Connect to the database
    conn = sqlite3.connect('cloud_storage.db')
    c = conn.cursor()

    # Check if email is already registered
    c.execute("SELECT * FROM Users WHERE email=?", (email,))
    existing_user = c.fetchone()
    if existing_user:
        conn.close()
        flash("User with this email already exists. Please use a different email.")
        return load_home_page()
    else:
        # Insert user into database
        # Insert the user into the database
        c.execute("INSERT INTO Users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, password_hash))

        # Commit changes and close connection
        conn.commit()
        conn.close()
        flash("Registration successful! Please log in.", "success")
        return render_template("index.html", show_alert_account_created=True)

def hash_password(password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    return hashed_password

def check_password(hashed_password, user_password):
    return bcrypt.check_password_hash(hashed_password, user_password)


@app.route('/update_account', methods=['POST'])
def update_account():
    username = request.form.get('username')
    phone = request.form.get('phone')
    address = request.form.get('address')
    payment = request.form.get('payment')

    conn = sqlite3.connect('cloud_storage.db')
    c = conn.cursor()

    user = session.get('user')
    
    session['user'] = {
        'user_id': user['user_id'],
        'username': username,
        'email': user['email'],
        'password': user['password'],
        'phone': phone,
        'address': address,
        'payment_info': payment
    }

    c.execute('''
        UPDATE Users
        SET username=?, phone=?, address=?, payment_info=?
        WHERE user_id=?
    ''', (username, phone, address, payment, user['user_id']))

    conn.commit()
    conn.close()

    flash("Account information updated successfully.", "success")
    return redirect(url_for('load_account_page'))


@app.route('/change_password', methods=['POST'])
def change_password():
    old_password = request.form.get('oldPassword')
    new_password = request.form.get('newPassword')
    confirm_password = request.form.get('confirmPassword')

    # Retrieve the user's current hashed password from the database
    conn = connect_db()
    c = conn.cursor()

    if new_password == confirm_password:
        session['user']['password'] = confirm_password

    c.execute("SELECT password_hash FROM Users WHERE user_id=?",
              (session['user']['user.id'],))
    current_password_hash = c.fetchone()[0]

    conn.close()

    if check_password(current_password_hash, old_password):
        if new_password == confirm_password:
            new_password_hash = hash_password(new_password)

            conn = connect_db()
            c = conn.cursor()

            c.execute('''
                UPDATE Users
                SET password_hash=?
                WHERE user_id=?
            ''', (new_password_hash, session['user.id']))

            conn.commit()
            conn.close()

            flash("Password changed successfully.", "success")
            return redirect(url_for('load_account_page'))
        else:
            flash("New passwords do not match. Please try again.", "error")
    else:
        flash("Incorrect current password. Please try again.", "error")

    return redirect(url_for('load_account_page'))



if __name__ == '__main__':
    app.run(debug=True)
