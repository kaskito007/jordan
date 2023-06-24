from flask import Blueprint
from flask import Blueprint, jsonify, abort, request
from ..models import  Housekeeper, db


import hashlib
import secrets

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

bp = Blueprint('housekeepers', __name__, url_prefix='/housekeepers')

# from ..models import Task, Room, Housekeeper, db
@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    housekeepers = Housekeeper.query.all() # ORM performs SELECT query
    result = []
    for h in housekeepers:
        result.append(h.serialize()) # build list of taks as dictionaries
    return jsonify(result) # return JSON respons


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    h = Housekeeper.query.get_or_404(id)
    return jsonify(h.serialize())

@bp.route('', methods=['POST'])
def create():
    # Check if the required properties are present in the request JSON
    if 'username' not in request.json or 'password' not in request.json:
        return abort(400)

    id = request.json.get('id')
    name = request.json.get('name')
    available = request.json.get('available')
    username = request.json['username']
    password = request.json['password']
    age = request.json.get('age')
    gender = request.json.get('gender')
    phone_number = request.json.get('phone_number')
    email = request.json.get('email')

    # Check username and password length requirements
    if len(username) < 3 or len(password) < 8:
        return abort(400)

    # Create a new Housekeeper object
    h = Housekeeper(
        id=id,
        name=name,
        available=available,
        username=username,
        password=password,
        age=age,
        gender=gender,
        phone_number=phone_number,
        email=email
    )

    db.session.add(h)  # Prepare CREATE statement
    db.session.commit()  # Execute CREATE statement

    return jsonify(h.serialize())