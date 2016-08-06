import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path = "", static_folder = "static")
try:
	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
	print('connected to heroku db')
except KeyError:
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Chimneyswift@localhost/postgres'
	print('connected to local db')
	
#all the line below does is stop a warning message from comming up	
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<Name %r>' % self.username	
		
@app.route('/')
def hello_world():
	return render_template('index.html')
	
@app.route('/LogIn', methods=['POST'])
def login():
	#user = User(request.form['username'], request.form['password'])
	username = request.form['username']
	password = request.form['password']
	
	Valid = False
	
	if(username != "" and password != ""):	
		currUser = User.query.filter_by(username=username).first()
		try:
			if(currUser.password == password):
				Valid = True
		except:
			Valid = False
	
	if(Valid):
		return render_template('avatar/avatar.html')
	else:
		return render_template('index.html', message="Invalid username or password")
	
@app.route('/SignUpPage', methods=['POST'])	
def signUpPage():
	return render_template('signUp.html')
	
	
@app.route('/SignUp', methods=['POST'])
def signUp():
	error = None
	username = request.form['username']
	password = request.form['password']
	
	if(username == "" or password == ""):
		error = "please enter a username and password"
		return render_template('signUp.html', error=error)
	
	try:
		user = User(username, password)
		db.session.add(user)
		db.session.commit()
		return render_template('index.html', message="You have successfully created an account")
	except:
		error = "username taken"
		return render_template('signUp.html', error=error)