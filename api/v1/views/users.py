#!/usr/bin/python3
"""
View for User objects that handles all default
RESTful API actions
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves a list of all User objects"""
    users = list(storage.all(User).values())
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def Get_User_By_Id(user_id):
    """Retrieves a user based on the id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User based on the id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new user"""
    if request.headers.get('Content-Type') != 'application/json':
        abort(400, "Not a JSON")
    if "email" not in request.get_json():
        abort(400, "Missing email")
    if "password" not in request.get_json():
        abort(400, "Missing password")
    user = User(**request.get_json())
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<users_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a user object based on the id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.headers.get('Content-Type') != 'application/json':
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
