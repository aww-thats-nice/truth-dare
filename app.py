import os
from flask import Flask, flash, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from random import random, randint
from werkzeug.urls import url_parse

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login = LoginManager(app)

NUMBER_OF_ROWS = 50

from models import Truth, Dare, Bingo, User, FulfillTask
from forms import LoginForm, RegistrationForm

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/card")
def card():
    return render_template("card.html", title="Play Truth or Dare", content="Click on the buttons below!")

@app.route("/card/truth")
def truth():
    prob = random()
    id_ = randint(1, NUMBER_OF_ROWS)

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
    id_ = randint(1, NUMBER_OF_ROWS)

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
    id_ = randint(1, NUMBER_OF_ROWS)
    title = "Do this today!"
    content = Dare.query.filter_by(id=id_).first().description
    return render_template("randomizer.html", title=title, content=content)

@app.route("/bingo")
@login_required
def bingo():
    bingo_array = Bingo.query.all()
    user_prog = list(map(lambda x: x.bingo_id, FulfillTask.query.filter_by(user_id=current_user.id).all()))
    return render_template("bingo.html", bingo_array=bingo_array, user_prog=user_prog)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        flash('Successfully logged in!')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('Successfully logged out!')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/check', methods=['POST'])
@login_required
def check():
    response = request.get_json()
    task = FulfillTask(user_id=current_user.id, bingo_id=response['id'])
    db.session.add(task)
    db.session.commit()
    flash('Bingo task checked!')
    return redirect(url_for('bingo'))

@app.route('/uncheck', methods=['POST'])
@login_required
def uncheck():
    response = request.get_json()
    task = FulfillTask.query.filter_by(user_id=current_user.id, bingo_id=response['id']).first()
    db.session.delete(task)
    db.session.commit()
    flash('Bingo task unchecked!')
    return redirect(url_for('bingo'))

if __name__ == "__main__":
    app.run(debug=True)
