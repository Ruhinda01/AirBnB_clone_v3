#!/usr/bin/python3
"""
New view for the link between Place objs
and Amenity objs that handles all default
RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities(place_id):
    """
    Retrieves a list of all Amenity objects
    of a Place
    Arg:
        place_id (str): Place id
    Returns:
        A JSON dictionary of Amenity objects
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amen_list = []
    for amenity in place.amenities:
        amen_list.append(amenity.to_dict())
    return jsonify(amen_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_place(place_id, amenity_id):
    """
    Deletes a amenity object based of place_id
    and amenity_id
    Args:
        place_id (str): Place id
        amenity_id (str): Amenity id
    Returns:
        A empty JSON dictionary with a 200 response
        A 404 response
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """
    Links an Amenity to a Place
    Args:
        place_id (str): Place id
        amenity_id (str): Amenity id
    Returns:
        A JSON dictionary with a 201 response
        A 404 response or 200 response
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
