from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qgeyxyqrnuxpyi:7fda5a2de7f65236bfa7538a84f3dd015c16a231779d6b7b551480e8918979b7@ec2-18-232-254-253.compute-1.amazonaws.com:5432/d6u7c86osmacim'

db = SQLAlchemy(app)

class Truth(db.Model):
	__tablename__ = "Truth"

	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	description = db.Column(db.String(200), nullable=False)

	def __init__(self, description):
		self.description = description

class Dare(db.Model):
	__tablename__ = "Dare"

	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	description = db.Column(db.String(200), nullable=False)

	def __init__(self, description):
		self.description = description

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
