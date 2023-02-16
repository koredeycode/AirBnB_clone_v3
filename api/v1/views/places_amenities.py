#!/usr/bin/python3
"""view for the link between place and amenity objects"""
from flask import jsonify, make_response, abort
from api.v1.views import app_views
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route('places/<place_id>/amenities/', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id=None):
    """Return info about a place amenity objects"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if storage_t == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]
    return make_response(jsonify(amenities), 200)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Delete the amenity of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if storage_t == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """link a amenity to a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if storage_t == "db":
        if amenity in place.amenities:
            make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_id.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
