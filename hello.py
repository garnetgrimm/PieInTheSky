from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlechemy

app = Flask(__name__, static_url_path = "", static_folder = "static")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLALchemy(app)

#dont forget to add sqlaclhemy to the freeze thing

@app.route('/')
def hello_world():
    return render_template('avatar/avatar.html')