from flask import Blueprint, jsonify, abort, request
from ..models import Task, Room, Housekeeper, db

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    Tasks = Task.query.all() # ORM performs SELECT query
    result = []
    for t in Tasks:
        result.append(t.serialize()) # build list of taks as dictionaries
    return jsonify(result) # return JSON respons

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    t = Task.query.get_or_404(id)
    return jsonify(t.serialize())

@bp.route('', methods=['POST'])
def create():
    # req body must contain room_number and house keeper name 
    if 'room_number' not in request.json or 'room_type' not in request.json:
        return abort(400)
    # user with id of user_id must exist
    Room.query.get_or_404(request.json['room_number'])
    # construct Task
    t = Task(
        room_number=request.json['room_number'],
        room_type=request.json['room_type'],
        assigned_to_name=request.json['assigned_to_name'],
    )
    db.session.add(t) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(t.serialize())



@bp.route('/tasks/<int:id>', methods=['PATCH'])
def update_task(id: int):
    task = Task.query.get_or_404(id)

    if 'room_number' in request.json:
        Room.query.get_or_404(request.json['room_number'])
        task.room_number = request.json['room_number']
    if 'room_type' in request.json:
        task.room_type = request.json['room_type']
    if 'assigned_to_name' in request.json:
        task.assigned_to_name = request.json['assigned_to_name']

    db.session.commit()

    return jsonify(task.serialize())



@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})
