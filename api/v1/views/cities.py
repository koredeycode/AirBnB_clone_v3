#!/usr/bin/python3
"""This is the module for the city views"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.state import State
from models.city import City
from models import storage


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_state_cities(state_id=None):
    """return info about the state cities objects"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]

    return make_response(jsonify(cities), 200)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(id):
    """return info about a city objects"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return make_response(jsonify(city.to_dict()), 200)


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id=None):
    """delete a city objects"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city(state_id=None):
    """create a city object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if "name" not in data:
        abort(400, description="Missing name")

    city = City(**data)
    city.state_id = state.id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id=None):
    """update the city object"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
