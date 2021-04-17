from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean())

    def __init__(self, email, password, is_active):
        self.email = email
        self.password = password
        self.is_active = is_active

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "userId": self.userId,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    idCharacter = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)

    def __init__(self, name, weight, height):
        self.name = name
        self.weight = weight
        self.height = height

class Planets(db.Model):
    idPlanet = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    Population = db.Column(db.Integer)
    sizeKm = db.Column(db.Float)

    def __init__(self, name, Population, sizeKm):
        self.name = name
        self.Population = Population
        self.sizeKm = sizeKm

class Favorities(db.Model):
    favoriteId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, ForeignKey(User.userId))
    planetId = db.Column(db.Integer, ForeignKey(Planets.idPlanet))
    characterId = db.Column(db.Integer, ForeignKey(Characters.idCharacter))

    def __init__(self, userId, planetId, characterId):
        self.userId = userId
        self.planetId = planetId
        self.characterId = characterId

# Database Schemas
class CharacterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Characters

class PlanetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Planets

class FavoritiesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Favorities