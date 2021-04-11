from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float

db = SQLAlchemy()

class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "userId": self.userId,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    idCharacter = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)

class Planets(db.Model):
    idPlanet = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    Population = db.Column(db.Integer)
    sizeKm = db.Column(db.Float)

class Favorities(db.Model):
    favoriteId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(ForeignKey(User.userId))
    planetId = db.Column(ForeignKey(Planets.idPlanet))
    characterId = db.Column(ForeignKey(Characters.idCharacter))