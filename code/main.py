from flask import render_template, request, redirect, session, url_for,flash, Flask 
from flask_login import login_required
from user import createAccount
from auth import auth_bp, login_manager
from fitnessareas import areas_bp
from whereshouldigo import WhereShouldIGo_bp
from checkin import checkin_bp
import sqlite3
from models import app, db
#from flask_cors import CORS # frontend
from flask import jsonify # frontend

# frontend
#app = Flask(__name__)
#CORS(app)


app.secret_key = 'your_secret_key'
app.register_blueprint(auth_bp)
app.register_blueprint(checkin_bp)
app.register_blueprint(WhereShouldIGo_bp)
app.register_blueprint(areas_bp)
login_manager.init_app(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

items = [
        {'category': 'Nature Reserves', 'image': 'image1', 'description': 'protected areas of importance for flora, fauna, or features of geological or other special interest'},
        {'category': 'Parks', 'image': 'image2', 'description': 'areas of natural, semi-natural or planted space for  enjoyment and recreation'},
        {'category': 'Wildlife Reserves', 'image': 'image3', 'description': 'large areas of land where wild animals live safely' }
    ]
@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("You must be logged in to view that page.")
    return redirect(url_for('auth.login'))


@app.route("/") #home page before login 
def home():
    return render_template("home.html")

@app.route("/user") #userpage
def user():
    # get the username from the session
    username = session.get('username')
    #print(session.get('username')) 
    # if the user is not logged in, redirect to the login page
    if not username:
        return redirect(url_for('auth.login'))
    return render_template('user.html', username=username)

@app.route('/createAccount', methods=['GET', 'POST'])
def createAccountView():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        points = 0
        
        if password1 != password2:
            error = 'Passwords do not match'
            return jsonify({'message': 'Passwords do not match'}), 401

        try:
            createAccount(username, password1, points)
            print("sign up successful")
            return {'message': 'success'}
        except ValueError as e:
            error = str(e)
            return jsonify({'message': 'Error!'}), 401

    else:
        error= None
        return render_template('createAccount.html',error=error)

@app.route('/directions') #get directions to destination from current location
def getDirections():
    #user login required, idk how todo this lol
    travel={'destination': 'Changi Airport', 'mode': 'TRANSIT'} 
    #placeholder, should be selected location and mode of transport instead
    return render_template('directions.html', travel=travel)

@app.route('/addLocation') #clicking on map to create location
def addLocation():
    #admin login required, idk how todo this lol
    return render_template('addLocation.html')

@app.route('/handle_click', methods=['POST']) #for getting location input only, don't open this
def handle_click():
    data = request.get_json()
    name = data['name']
    latitude = data['latitude']
    longitude = data['longitude']
    points = data['points']
    category = data['category']
    description = data['description']
    conn=sqlite3.connect('C:/Users/Bakase/Documents/GitHub/test2/code/DB/areas.db') #change to appropriate db path
    c = conn.cursor()
    c.execute('INSERT INTO areas (name, latitude, longitude, points, category, description) VALUES (?, ?, ?, ?, ?, ?)', (name, latitude, longitude, points, category, description))
    conn.commit()
    conn.close()
    print('Success')  # print a success message
    message = 'Successfully added location: ' + name
    return jsonify({'result': 'Success', 'message': message})

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    return render_template('home.html')

# General error handler for all status codes
@app.errorhandler(Exception)
def handle_error(e):
    return render_template('error.html', error=str(e)), getattr(e, 'code', 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0')


app.run()
#test commit