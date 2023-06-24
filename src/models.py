from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()
from sqlalchemy.orm import relationship 

class Guest(db.Model):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    phone_number = db.Column(db.String(128), nullable=False)
    check_in_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    check_out_time = db.Column(db.DateTime)


class Room(db.Model):
    __tablename__ = 'rooms'

    number = db.Column(db.Integer, primary_key=True, unique = True, autoincrement=True)
    capacity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean, default=True)
    room_type = db.Column(db.String(20), nullable=False)

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_number = db.Column(db.Integer, db.ForeignKey('rooms.number'), nullable=False)
    room_type = db.Column(db.String(20), db.ForeignKey('rooms.room_type'), nullable=False)
    assigned_to_name = db.Column(db.String(128), db.ForeignKey('housekeepers.name'), nullable=True)
    assigned_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, room_number, room_type, assigned_to_name):
        self.room_number = room_number
        self.room_type = room_type
        self.assigned_to_name = assigned_to_name
        self.assigned_at = datetime.utcnow()
        self.completed = False
    
    def serialize(self):
        return {
            'id': self.id,
            'room_number': self.room_number,
            'room_type': self.room_type,
            'assigned_to_name': self.assigned_to_name,
            'assigned_at': self.assigned_at.isoformat(),
            'completed': self.completed
        }
    
class Housekeeper(db.Model):
    __tablename__ = 'housekeepers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique = True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone_number = db.Column(db.String(82), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    available = db.Column(db.Boolean, default=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    tasks = relationship('Task', backref='housekeeper')

    def __init__(self,id,name,age,gender,phone_number,email,available,username,password):
        self.id=id
        self.name=name
        self.age=age
        self.gender=gender
        self.phone_number=phone_number
        self.email=email
        self.available=available
        self.username=username
        self.password=password
        
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'phone_number': self.phone_number,
            'email': self.email,
            'available': self.available,
            'username': self.username,
            'password': self.password
        }