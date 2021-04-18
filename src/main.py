import os
import json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, ma, User
from models import Characters, Planets, Favorities
from models import CharacterSchema, PlanetSchema, FavoritiesSchema

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret"  
jwt = JWTManager(app)
MIGRATE = Migrate(app, db)
db.init_app(app)
ma.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/token', methods=['POST'])
def create_token():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user = db.session.query(User).filter(User.email==email, User.password==password).first()
    if User is None:
        return jsonify({'message': 'email or password wrong'}), 401
    
    access_token = create_access_token(identity=user.userId) 
    return jsonify(
        {
        'token': access_token, 'user id': user.userId
        })

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({"id": user.userId, "username": user.email }), 200

@app.route('/user', methods=['POST'])
def create_user():
    email = request.json['email']
    password = request.json['password']
    is_active = request.json['is_active']
    
    new_user = User(email, password, is_active)
    db.session.add(new_user)
    db.session.commit()
    return 'New user created succesfully'

@app.route('/characters/create', methods=['POST'])
def create_characters():
    name = request.json['name']
    height = request.json['height']
    weight = request.json['weight']

    new_character = Characters(name, height, weight)
    db.session.add(new_character)
    db.session.commit()

    return 'Character created sucessfully'

@app.route('/planets/create', methods=['POST'])
def create_planets():
    name = request.json['name']
    population = request.json['population']
    sizeKm = request.json['sizeKm']

    new_planet = Planets(name, population, sizeKm)
    db.session.add(new_planet)
    db.session.commit()

    return 'Planets created succesfully'

@app.route('/characters/<int:id>', methods=['GET'])
def get_character(id):
    character = Characters.query.get(id)
    characters_schema = CharacterSchema()
    output = characters_schema.dump(character)
    return jsonify(output)

@app.route('/characters', methods=['GET'])
def get_characters():
    characters_all = Characters.query.all()
    characters_schema = CharacterSchema(many=True)
    output = characters_schema.dump(characters_all)
    return jsonify(output)

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    planet = Planets.query.get(id)
    planet_schema = PlanetSchema()
    output = planet_schema.dump(planet)
    return jsonify(output)

@app.route('/planets', methods=['GET'])
def get_planets():
    planets_all = Planets.query.all()
    planets_schema = PlanetSchema(many=True)
    output = planets_schema.dump(planets_all)
    return jsonify(output)

@app.route('/favoritie/create', methods=['POST'])
def add_favorite():
    userId = request.json['userId']
    planetId = request.json['planetId']
    characterId = request.json['characterId']

    new_favoritie = Favorities(userId, planetId, characterId)
    db.session.add(new_favoritie)
    db.session.commit()
    return 'New Favorite added successfully'

@app.route('/favorities', methods=['GET'])
def get_favorities():
    favorities_all = Favorities.query.all()
    favorities_schema = FavoritiesSchema(many=True)
    output = favorities_schema.dump(favorities_all)
    return jsonify(output)

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)