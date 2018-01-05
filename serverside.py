from flask import Flask
import random
from flask import jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import os
from flask import render_template
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash

from flask_cors import CORS
app = Flask(__name__)
CORS(app)

#the below 3 lines simply causes only errors and print statements to be logged to console
#otherwise every freakin request will be logged
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, static_url_path = "", static_folder = "static")
#dialect+driver://username:password@host:port/database
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
	__tablename__ = 'user'

	id = db.Column(db.Integer, primary_key=True)
	FirstName = db.Column(db.String())
	LastName = db.Column(db.String())
	Username = db.Column(db.String())
	Password = db.Column(db.String())
	InGame = db.Column(db.Boolean())
	InLobby = db.Column(db.String())
	
	def __init__(self, FirstName, LastName, Username, Password):
		self.FirstName = FirstName
		self.LastName = LastName
		self.Username = Username
		self.set_password(Password)
		self.InGame = None
		self.InLobby = None
		
	def set_password(self, password):
		self.Password = generate_password_hash(password)
	
	def check_password(self, password):
		return check_password_hash(self.Password, password)
		
	def __repr__(self):
		return '<id {}>'.format(self.id)
		
class Game(db.Model):
	__tablename__ = 'game'

	id = db.Column(db.Integer, primary_key=True)
	Owner = db.Column(db.String())
	Players = db.Column(db.String())
	Targets = db.Column(db.String())
	Started = db.Column(db.Boolean)
	Password = db.Column(db.String())
	
	def __init__(self, Owner, Password):
		self.Owner = Owner
		self.Players = Owner
		self.Targets = ""
		self.Password = Password
		Started = False

	def __repr__(self):
		return '<id {}>'.format(self.id)

def generateList(names):
	random.shuffle(names)
	targets = names[:]
	targets.append(targets[0])
	del targets[0]
	
	return(names, targets)
	
def killPlayer(player, list):
	newTarget = list[1][list[0].index(player)]
	killer = list[0][list[1].index(player)]
	
	newTI = list[1].index(newTarget)
	newKI = list[0].index(killer)
	
	list[1][newKI] = newTarget
	del[list[1][newTI]]
	del[list[0][newTI]]
	
	return(list)

@app.route('/')
def hello_world():
	#names = [ "Garnet", "Xavier", "David" ]
	#list = generateList(names)
	#list = killPlayer("Garnet", list)
	
	#jsonify
	#return str(str(list[0]) + '<br>' + str(list[1]));
	#return "Users: " + str(User.query.filter_by().first().Username)
	return "Hello World!"

@app.route('/testing/signup')
def signupFORM():
	return render_template('signup.html')
	
@app.route('/testing/addPlayer')
def addPlayerFORM():
	return render_template('addPlayer.html')

@app.route('/testing/removePlayer')
def removePlayerFORM():
	return render_template('removePlayer.html')
	
@app.route('/testing/createLobby')
def createLobbyFORM():
	return render_template('createLobby.html')
	
@app.route('/testing/removeLobby')
def removeLobbyFORM():
	return render_template('removeLobby.html')
	
@app.route('/testing/startGame')
def startGameFORM():
	return render_template('startGame.html')

def addHeader(resp):	
	response = jsonify(resp)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response
	
	
@app.route('/createLobby', methods = ['POST'])
def createLobby():
	r = ""
	try:
		u = User.query.filter_by(Username=request.form.get('un')).first()
		loggedIN = str(u.check_password(request.form.get('pw')))
		if(loggedIN):
			g = Game.query.filter_by(Owner=request.form.get('un')).first()
			if(g == None):
				newGame = Game(request.form.get('un'), request.form.get('lpw'))
				db.session.add(newGame)
				u.InLobby = request.form.get('un') + "!" + request.form.get('lpw')
				db.session.commit()
				r = "P"
			else:
				r = "E3"
		else:
			r = "E2"
	except:
		r = "E1"
	return addHeader(r)
	
@app.route('/getPlayers', methods = ['POST'])
def getPlayers():
	r = ""
	if(True):
		u = User.query.filter_by(Username=request.form.get('un')).first()
		loggedIN = str(u.check_password(request.form.get('pw')))
		if(loggedIN):
			g = Game.query.filter_by(Owner=request.form.get('hn')).first()
			if(g != None):
				if(g.Password == request.form.get('lpw')):
					r = g.Players.split('!')
				else:
					r = "E4"
			else:
				r = "E3"
		else:
			r = "E2"
	else:
		r = "E1"
	
	return addHeader(r)
	
@app.route('/removeLobby', methods = ['POST'])
def removeLobby():
	r = ""
	#outdated
	try:
		u = User.query.filter_by(Username=request.form.get('un')).first()
		loggedIN = str(u.check_password(request.form.get('pw')))
		if(loggedIN):
			g = Game.query.filter_by(Owner=request.form.get('un')).first()
			if(g != None):
				db.session.delete(g)
				db.session.commit()
				r = "P"
			else:
				r = "E3"
		else:
			r = "E2"
	except:
		r = "E1"
		
	return addHeader(r)	
	
@app.route('/joinLobby', methods = ['POST'])
def joinLobby():
	r = ""
	try:
		u = User.query.filter_by(Username=request.form.get('un')).first()
		loggedIN = str(u.check_password(request.form.get('pw')))
		if(loggedIN):
			g = Game.query.filter_by(Owner=request.form.get('hn')).first()
			if(g != None):
				if(g.Password == request.form.get('lpw')):
					g.Players+=("!"+request.form.get('un'))
					
					u.InLobby = request.form.get('hn') + "!" + request.form.get('lpw')
					db.session.commit()
					r = "P"
				else:
					r = "E4"
			else:
				r = "E3"
		else:
			r = "E2"
	except:
		r = "E1"
	
	return addHeader(r)
	
@app.route('/leaveLobby', methods = ['POST'])
def leaveLobby():
	r = ""
	try:
		u = User.query.filter_by(Username=request.form.get('un')).first()
		loggedIN = str(u.check_password(request.form.get('pw')))
		if(loggedIN):
			g = Game.query.filter_by(Owner=request.form.get('hn')).first()
			if(g != None):
				p = g.Players.split("!")
				p = p.remove('un')
				p = p.join("!")
				g.Players = p
				db.session.commit()
			else:
				r = "E3"
		else:
			r = "E2"
	except:
		r = "E1"
	
	return addHeader(r)	
	
@app.route('/removePlayer', methods = ['POST'])
def removePlayer():
	r = ""
	try:
		u = User.query.filter_by(Username=request.form.get('hostname')).first()
		loggedIN = str(u.check_password(request.form.get('password')))
		if(loggedIN):
			g = Game.query.filter_by(Owner=request.form.get('hostname')).first()
			if(g != None):
				if request.form.get('username') == request.form.get('hostname'):
					return "E5"
				p = g.Players.split('!')
				for i in range(0, len(p)):
					if p[i] == request.form.get('username'):
						del p[i]
						g.Players = str.join("!", p)
						db.session.commit()
						r = "P"
						break
				if r != "P":
					r = "E4"
			else:
				r = "E3"
		else:
			r = "E2"
	except:
		r = "E1"
	
	return addHeader(r)
	
@app.route('/startGame', methods = ['POST'])
def startGame():
	r = ""
	
	try:
		u = User.query.filter_by(Username=request.form.get('un')).first()
		loggedIN = str(u.check_password(request.form.get('pw')))
		if(loggedIN):
			g = Game.query.filter_by(Owner=request.form.get('un')).first()
			if(g != None):
				p = g.Players.split('!')
				for i in range(0, len(p)):
					User.query.filter_by(Username=p[i]).first().InGame = True
				list = generateList(p)
				g.Players = str.join("!", list[0])
				g.Targets = str.join("!", list[1])
				g.Started = True
				db.session.commit()
				r = "P"
			else:
				r = "E3"
		else:
			r = "E2"
	except:
		r = "E1"
		
	return addHeader(r)
	
@app.route('/getTarget', methods = ['POST'])
def getTarget():
	r = ""
	if(True):
		g = Game.query.filter_by(Owner=request.form.get('hn')).first()
		if(g.Password == request.form.get('lpw')):
			i = g.Players.split('!').index(request.form.get('un'))
			t = g.Targets.split('!')[i]
			t = User.query.filter_by(Username=t).first()
			t = t.FirstName + " " + t.LastName
			
			u = User.query.filter_by(Username=request.form.get('un')).first()
			loggedIN = str(u.check_password(request.form.get('pw')))
			if loggedIN == "True":
				r = t
			else:
				r = "E3"
		else:
			r ="E2"
	else:
		r = "E1"
	
	return addHeader(r)

@app.route('/login', methods = ['POST'])
def login():
	u = User.query.filter_by(Username=request.form.get('un')).first()
	r = ""
	if(u != None):
		loggedIN = str(u.check_password(request.form.get('pw')))
		if loggedIN == "True":
			r = "P"
		else:
			r ="E2"
	else:
		r = "E1"
		
	return addHeader(r);
		
@app.route('/getPlayerStats', methods = ['POST'])
def getPlayerStats():
	u = User.query.filter_by(Username=request.form.get('un')).first()
	loggedIN = str(u.check_password(request.form.get('pw')))
	if loggedIN == "True":
		hn = None
		lpw = None
		
		if(u.InLobby != None):
			hn = u.InLobby.split("!")[0]
			lpw = u.InLobby.split("!")[1]
	
		playerData = {
			'un':u.Username, 
			'pw':u.Password,
			'fn':u.FirstName, 
			'ln':u.LastName, 
			'ig': u.InGame,
			'hn': hn,
			'lpw': lpw
		}
		return addHeader(playerData)
	else:
		addHeader("E1")

@app.route('/signup', methods = ['POST'])
def sign_up():
	FN=request.form.get('fn')
	LN=request.form.get('ln')
	UN=request.form.get('un')
	PW=request.form.get('pw')
	u = User.query.filter_by(Username=request.form.get('un')).first()
	if(u == None):
		newUser = User(FN,LN,UN, PW)
		db.session.add(newUser)
		db.session.commit()
		return addHeader("P")
	#jsonify
	return addHeader("E1")
	
@app.route('/startGame/<ON>')
def start_game(ON):
	newGame = User(ON)
	db.session.add(newGame)
	db.session.commit()
	#jsonify
	return addHeader(str(FN))
