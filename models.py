from app import db

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
