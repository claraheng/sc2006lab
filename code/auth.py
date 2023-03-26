from flask import Flask,Blueprint, render_template, request, redirect, url_for, flash,session
from flask_login import LoginManager, login_user, logout_user, login_required
from user import User, find_by_username
import sqlite3
from flask_cors import CORS # frontend
from flask import jsonify # frontend

# frontend
app = Flask(__name__)
CORS(app)

auth_bp = Blueprint('auth', __name__)
login_manager = LoginManager()
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(username):
        connection=sqlite3.connect('DB/users.db')
        cursor=connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username=?',(username,))
        user_data=cursor.fetchone()
        connection.close()
        
        if not user_data:
            return None
        
        return User(user_data[0],user_data[1],user_data[2])

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = find_by_username(username)
<<<<<<< HEAD
        if user and user.check_password(password):
=======
        if username == "admin" and password=="admin":
            return render_template('admin.html')
        
        elif user and user.check_password(password):

>>>>>>> 83fc0e2 (done show points and created admin page)
            session['username'] = user.username
            login_user(user)
            return jsonify({'message':'Logged in successfully'})
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

