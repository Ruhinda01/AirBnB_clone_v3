#!/usr/bin/python3
"""
View for Amenity objs that
handles all RESTfil API actions
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def show_amenities():
    """Retrieves the list of all amenity objects"""
    amen_list = []
    amenities = storage.all(Amenity)
    for amen in amenities.values():
        amen_list.append(amen.to_dict())
    return jsonify(amen_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def show_amenity(amenity_id):
    """Retrieves a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an amenity obj"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an amenity obj"""
    if request.headers.get('Content-Type') != 'application/json':
        abort(400, "Not a JSON")
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    # data = request.get_json()
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates amenity obj based on id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.headers.get('Content-Type') != 'application/json':
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
