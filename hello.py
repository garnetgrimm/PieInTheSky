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

def getBadgeString(badges):
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
	return bstring
	

def getPostString():
	pstring = ""
	for p in range(0, 2):
		currPost = Post.query.filter_by(id="1").first()
		pstring += currPost.img
		pstring += "[BSPL]"
		pstring += currPost.date
		pstring += "[BSPL]"
		pstring += currPost.desc
		pstring += "[BSPL]"
		pstring += currPost.comments
		pstring += "{BSPL}"
	pstring = pstring[:-6]
	pstring += ""
	return pstring

class curr():
	currentUser = ""
	searchedUser = ""

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

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	#('3DPrinter.png', 'mm_dd_yyyy','I 3D printed something!!!', 'garnet: awesome![SPL]testuser41: cool');
	#if no pic source given, dont try to add pic
	
	img = db.Column(db.String())
	date = db.Column(db.String(30))
	desc = db.Column(db.String())
	comments = db.Column(db.String())
	user = db.Column(db.String(80))
	
	def __init__(self, img, date, desc, comments, user):
		self.img = img
		self.date = date
		self.desc = desc
		self.comments = comments
		self.user = user
	
	def __repr__(self):
		return '<' + str(self.id) + '>'	
		
@app.route('/')
def hello_world():
	return render_template('index.html')
	
@app.route('/Badges', methods=['POST'])
def badges():
	user = User.query.filter_by(username=curr.currentUser).first()
	badges = user.badges.split(",")
	bstring = getBadgeString(badges)
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

@app.route("/News", methods=['POST'])
def news():
	print(getPostString())
	return render_template('news.html')
	
@app.route("/searchUser", methods=['POST'])
def search():
	#search needs work for sure
	key = request.form['user']
	res = User.query.filter_by(username=key).first()
	user = User.query.filter_by(username=curr.currentUser).first()
	
	try:
		curr.searchedUser = res.username
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
	
	badge = Badge(name, pic, c1, c2, desc)
	db.session.add(badge)
	db.session.commit()
	
	return home()

@app.route('/awardBadges', methods=['POST'])
def awardBadges():
	newBadges = request.form['selectedBadges']
	u = User.query.filter_by(username=curr.searchedUser).first()
	
	newBadges = newBadges.split(",")
	badges = ""
	
	for b in range(0, len(newBadges)):
		newBadges[b] = int(newBadges[b]) + 1
		badges += str(newBadges[b])
		badges += ","
	
	badges = badges[:-1]
	
	print(badges)
	
	u.badges = badges
	db.session.commit()
	
	return home()
	
@app.route('/getAllAwards', methods=['POST'])
def getAllAwards():
	user = User.query.filter_by(username=curr.currentUser).first() 
	oldbadges = User.query.filter_by(username=curr.searchedUser).first().badges 
	award = Badge.query.all()
	
	#error because of how bstring is stored
	bstring = []
	for i in range(0, len(award)):
		bstring.append(i + 1)
	
	award = getBadgeString(bstring)
	
	return render_template('home.html', user=user.username, admin=user.admin, oldbadges=oldbadges, award=award)

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
		user = User(username, password, "1:1:1:1:1:1:1:50", "1")
		#												  ^ seperate by commas, the id number of badges they have
		db.session.add(user)
		db.session.commit()
		return render_template('index.html', message="You have successfully created an account")
	except:
		error = "Username taken"
		return render_template('signUp.html', error=error)