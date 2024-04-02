#!/usr/bin/python3
"""
View for User objs that handles all
default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Gets all the users in storage
    Return: a list of jsonified users
    """
    users = storage.all(User)
    users_list = []
    for user in users.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def Get_User_By_Id(user_id):
    """Displays a user based on the id

    Parameters:
    user_id [str]: id of the user
    Return: A JSON dictionary or a 404 response
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a user based off the id

    Parameters:
    user_id [str]: id of the user
    Return:
    A empty JSON dictionary with 200
    response or a 404 response
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new user object
    Return:
    A JSON dictionary with 201 response
    or a 400 response
    """
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
    """Updates a user object based on the id

    Parameters:
    user_id [str]: id of the user
    Return:
    A JSON dictionary with 200 response
    or a 400 response
    """
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
