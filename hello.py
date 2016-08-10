import os, sys
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json

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

class curr():
	currentUser = ""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    avatar = db.Column(db.String(42))
    badges = db.Column(db.String(42))
    admin = db.Column(db.Boolean)
	
    def __init__(self, username, password, avatar, badges):
        self.username = username
        self.password = password
        self.avatar = avatar
        self.badges = badges
        self.admin = False
    def __repr__(self):
        return '<Name %r>' % self.username

class Badge(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	#('Default_Badge.png', '#654321','gray', "Log In", "You created a digital skypy account!");
	name = db.Column(db.String(30))
	picSrc = db.Column(db.String(80))
	color1 = db.Column(db.String(10))
	color2 = db.Column(db.String(10))
	desc = db.Column(db.String(200))
	
	def __init__(self, name, picSrc, color1, color2, desc):
		self.name = name
		self.picSrc = picSrc
		self.color1 = color1
		self.color2 = color2
		self.desc = desc
	
	def __repr__(self):
		return '<Name %r>' % self.name		
		
@app.route('/')
def hello_world():
	return render_template('index.html')
	
@app.route('/Badges', methods=['POST'])
def badges():
	user = User.query.filter_by(username=curr.currentUser).first()
	badges = user.badges.split(",", 1)
	bstring = ""
	for badgeNum in badges:
		currBadge = Badge.query.filter_by(id=badgeNum).first()
		bstring += currBadge.picSrc
		bstring += "[SPL]"
		bstring += currBadge.color1
		bstring += "[SPL]"
		bstring += currBadge.color2
		bstring += "[SPL]"
		bstring += currBadge.name
		bstring += "[SPL]"
		bstring += currBadge.desc
		bstring += "{SPL}"
	bstring = bstring[:-5]
	bstring += ""
	print(bstring)
	return render_template('badges.html', user=user.username, badges=bstring)
	
@app.route("/openAvatar", methods=['POST'])
def openAvatar():
	currUser = User.query.filter_by(username=curr.currentUser).first()
	return render_template('avatar/design_avatar.html', currAvatar=currUser.avatar, user=currUser.username)
	
@app.route("/saveAvatar", methods=['POST'])
def saveAvatar():
	currUser = User.query.filter_by(username=curr.currentUser).first()
	currUser.avatar = request.form['avatarString']
	db.session.commit()
	
	return render_template('avatar/design_avatar.html', currAvatar=request.form['avatarString'], user=currUser.username)

@app.route("/Home", methods=['POST'])
def home():
	user = User.query.filter_by(username=curr.currentUser).first()
	return render_template('home.html', user=user.username, admin=user.admin)

@app.route("/searchUser", methods=['POST'])
def search():
	#search needs work for sure
	key = request.form['user']
	res = User.query.filter_by(username=key).first()
	user = User.query.filter_by(username=curr.currentUser).first()
	
	try:
		return render_template('home.html', user=user.username, admin=user.admin, searchres=res.username)
	except:
		return render_template('home.html', user=user.username, admin=user.admin)
	
@app.route("/createBadge", methods=["POST"])
def createBadge():
	name = request.form['name']
	pic = request.form['picSrc']
	c1 = request.form['color1']
	c2 = request.form['color2']
	desc = request.form['desc']
	
	desc = desc.replace('\r', '')
	desc = desc.replace('\n', '')
	
	print(desc)
	
	badge = Badge(name, pic, c1, c2, desc)
	db.session.add(badge)
	db.session.commit()
	
	return home()
	
@app.route('/LogIn', methods=['POST'])
def login():
	username = request.form['username']
	password = request.form['password']
	
	curr.currentUser = username
	
	Valid = False
	
	currUser = User.query.filter_by(username=username).first()
	
	if(username != "" and password != ""):	
		try:
			if(currUser.password == password):
				Valid = True
		except:
			Valid = False
	
	if(Valid):
		return render_template('home.html', user=curr.currentUser, admin=currUser.admin)
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
		error = "Please enter a username and password"
		return render_template('signUp.html', error=error)
	
	try:
		user = User(username, password, "1:1:1:1:1:1:1", "1")
		#												  ^ seperate by commas, the id number of badges they have
		db.session.add(user)
		db.session.commit()
		return render_template('index.html', message="You have successfully created an account")
	except:
		error = "Username taken"
		return render_template('signUp.html', error=error)