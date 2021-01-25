from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Truth(db.Model):
    __tablename__ = "Truth"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(200), nullable=False)

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'description': self.description,
        }

class Dare(db.Model):
    __tablename__ = "Dare"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(200), nullable=False)

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'description': self.description,
        }

class Bingo(db.Model):
    __tablename__ = "Bingo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(200), nullable=False)

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'description': self.description,
        }

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)   

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class FulfillTask(db.Model):
    __tablename__ = "FulfillTask"

    # TODO: Implement foreign key
    user_id = db.Column(db.Integer, primary_key=True)
    bingo_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<user {} completes task {}>'.format(self.user_id, self.bingo_id)
    
    def serialize(self):
        return {
            'user_id': self.user_id, 
            'bingo_id': self.bingo_id,
        }

