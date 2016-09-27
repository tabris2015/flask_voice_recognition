import json
from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/flask_movie'
app.debug=True

db = SQLAlchemy(app)


###############################
## MODELS ##
class User(db.Model):
	"""docstring for User"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)

	def __init__(self, username, email):
		self.username = username
		self.email = email

	def __repr__(self):
		return '<User %r>' % self.username

class Measurement(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	value = db.Column(db.Integer, default=0)
	def __init__(self, value):
		self.value = value

	def __repr__(self):
		return '<Measurement %r>' % self.value

class Command(db.Model):
	"""docstring for Command"""
	id = db.Column(db.Integer, primary_key=True)
	shape = db.Column(db.Integer)
	color = db.Column(db.Integer)
	size = db.Column(db.Integer)
	def __init__(self, shape, color, size):
		self.shape = shape
		self.color = color
		self.size = size

	def __repr__(self):
		return '<Command (%r,%r,%r) >' % (self.shape, self.color, self.size)
		

class Text(db.Model):
	"""docstring for Text"""
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(400))
	timestamp = db.Column(db.DateTime)

	def __init__(self, text, timestamp):
		self.text = text
		self.timestamp = timestamp

	def __repr__(self):
		return '<Text %r>' % self.text


		
###############################
## VIEWS ##
@app.route('/')
def index():
	users = User.query.all()
	return render_template('add_user.html', users=users)

@app.route('/post_user', methods=['POST', 'GET'])
def post_user():
	user = User(request.form['username'], request.form['email'])
	print user

	db.session.add(user)
	print "added user"
	db.session.commit()
	print "commit to the database"
	

	return redirect(url_for('index'))

@app.route('/api/command', methods=['POST', 'GET'])
def get_command():
	if request.method == 'POST':
		command = Command(
							request.form['shape'],
							request.form['color'],
							request.form['size'])
		db.session.add(command)
		db.session.commit()
		print "added command!"
		return "success!"
	elif request.method == 'GET':
		commands = Command.query.all()
		command = commands[0]
		print command
		return render_template('commands.html', commands=commands)


@app.route('/json/command', methods=['POST', 'GET'])
def get_command_json():
	if request.method == 'POST':
		command = Command(
							request.form['shape'],
							request.form['color'],
							request.form['size'])
		db.session.add(command)
		db.session.commit()
		print "added command!"
		return "success!"
	elif request.method == 'GET':
		commands = Command.query.all()
		commands = convertCommands(commands)
		#js = json.dumps(commands)
		#resp = Response(js, status=200, mimetype='application/json')
		return jsonify({'commands': commands})
	
@app.route('/json/text', methods=['POST', 'GET'])
def text_json():
	if request.method == 'POST':
		text = Text(request.form['text'], datetime.utcnow())
		db.session.add(text)
		db.session.commit()
		print "added text!"
		return "success!"
	elif request.method == 'GET':
		texts = Text.query.all()
		texts = convertTexts(texts)
		#js = json.dumps(commands)
		#resp = Response(js, status=200, mimetype='application/json')
		return jsonify({'text': texts[-1]})
	
###############################

####### helpers

def convertCommands(commands):
	commands_list = []
	for command in commands:
		command_dict = {
						'shape': int(command.shape),
						'color': int(command.color),
						'size': int(command.size)
						}
		commands_list.append(command_dict)
	return commands_list

def convertTexts(texts):
	texts_list = []
	for text in texts:
		text_dict = {'text': str(text.text), 'timestamp': str(text.timestamp)}
		texts_list.append(text_dict)
	return texts_list
##################
if __name__ == "__main__":
	app.run()
