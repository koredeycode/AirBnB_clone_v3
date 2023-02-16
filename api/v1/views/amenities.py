#!/usr/bin/python3
"""This is the module for the amenity views"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenities():
    """return info about the amenity objects"""
    amenities = storage.all(Amenity).values()
    amenities = [amenity.to_dict() for amenity in amenities]
    return (jsonify(amenities))


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    """return info about a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return make_response(jsonify(amenity.to_dict()), 200)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """delete a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities/", methods=['POST'], strict_slashes=False)
def create_amenity():
    """create a amenity object"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if "name" not in data:
        abort(400, description="Missing name")

    amenity = Amenity(**data)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id=None):
    """update the amenity object"""
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
