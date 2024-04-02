#!/usr/bin/python3
"""create a new view for City objects
that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_state_cities(state_id):
    """Retrives a states cities"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrives cities using a city id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a city using a city id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def creates_city(state_id):
    """City in  a state using a state_id"""
    if request.headers.get('Content-Type') != 'application/json':
        abort(400, "Not a JSON")

    if "name" not in request.get_json():
        abort(400, "Missing name")

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    Add_data = {'state_id': f'{state_id}'}
    data = request.get_json()
    data.update(Add_data)
    city = City(**request.get_json())
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a city object"""
    if request.headers.get('Content-Type') != 'application/json':
        abort(400, "Not a JSON")

    if "name" not in request.get_json():
        abort(400, "Missing name")

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    city = City(**request.get_json())
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
