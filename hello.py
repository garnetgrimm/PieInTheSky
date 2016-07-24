from flask import Flask, render_template
app = Flask(__name__, static_url_path = "", static_folder = "imgs")

@app.route('/')
def hello_world():
    return render_template('avatar/avatar.html')