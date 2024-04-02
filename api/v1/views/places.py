#!/usr/bin/python3
"""Creates a new view for Place objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def Get_City_Places(city_id):
    """Retrives a city's places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def Get_Place(place_id):
    """Retrives place using a place id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def Delete_Place(place_id):
    """Deletes a place using a place id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def Creates_place(city_id):
    """Creates a place in a city using a city_id"""
    if request.headers.get('Content-Type') != 'application/json':
        abort(400, "Not a JSON")

    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")

    if "name" not in request.get_json():
        abort(400, "Missing name")

    user = storage.get(User, request.get_json().get('user_id'))
    if user is None:
        abort(404)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    Add_data = {'city_id': f'{city_id}'}
    data = request.get_json()
    data.update(Add_data)
    place = Place(**request.get_json())
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def Update_place(place_id):
    """Updates a place object"""
    if request.headers.get('Content-Type') != 'application/json':
        abort(400, "Not a JSON")

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place = City(**request.get_json())
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'state_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
