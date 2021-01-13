import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from random import random, randint

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Truth, Dare

@app.route("/")
def home():
    return render_template("home.html", title="Play Truth or Dare", content="Click on the buttons below!")

@app.route("/truth")
def truth():
    prob = random()
    id_ = randint(1, 100)

    if prob < 0.7:  # generate truth
        title = "Truth"
        content=Truth.query.filter_by(id=id_).first().description
    else:  # generate dare
        title = "Dare"
        content=Dare.query.filter_by(id=id_).first().description
    
    return render_template("home.html", title=title, content=content)

@app.route("/dare")
def dare():
    prob = random()
    id_ = randint(1, 100)

    if prob < 0.7:  # generate dare
        title = "Dare"
        content=Dare.query.filter_by(id=id_).first().description
    else:  # generate truth
        title = "Truth"
        content=Truth.query.filter_by(id=id_).first().description

    return render_template("home.html", title=title, content=content)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
