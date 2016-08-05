import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path = "", static_folder = "static")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLALchemy(app)

@app.route('/')
def hello_world():
    return render_template('avatar/avatar.html')