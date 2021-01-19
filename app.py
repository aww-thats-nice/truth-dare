import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from random import random, randint

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Truth, Dare, Bingo

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/card")
def card():
    return render_template("card.html", title="Play Truth or Dare", content="Click on the buttons below!")

@app.route("/card/truth")
def truth():
    prob = random()
    id_ = randint(1, 100)

    if prob < 0.7:  # generate truth
        title = "Truth"
        content = Truth.query.filter_by(id=id_).first().description
    else:  # generate dare
        title = "Dare"
        content = Dare.query.filter_by(id=id_).first().description
    
    return render_template("card.html", title=title, content=content)

@app.route("/card/dare")
def dare():
    prob = random()
    id_ = randint(1, 100)

    if prob < 0.7:  # generate dare
        title = "Dare"
        content = Dare.query.filter_by(id=id_).first().description
    else:  # generate truth
        title = "Truth"
        content = Truth.query.filter_by(id=id_).first().description

    return render_template("card.html", title=title, content=content)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/randomizer")
def randomizer():
    return render_template("randomizer.html", title="Generate a Random Act of Kindness", content="Click the button below!")

@app.route("/randomizer/generate")
def generate():
    id_ = randint(1, 100)
    title = "Do this today!"
    content = Dare.query.filter_by(id=id_).first().description
    return render_template("randomizer.html", title=title, content=content)

@app.route("/bingo")
def bingo():
    bingo_array = Bingo.query.all()
    return render_template("bingo.html", bingo_array=bingo_array)

if __name__ == "__main__":
    app.run(debug=True)
