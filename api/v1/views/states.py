#!/usr/bin/python3
"""contains the views for the state endpoint"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.state import State
from models import storage


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    """return info about the state objects"""
    states = storage.all(State).values()
    states = [state.to_dict() for state in states]
    return (jsonify(states))


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """return info about the state objects"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return make_response(jsonify(state.to_dict()), 200)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """delete the state objects"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/", methods=['POST'], strict_slashes=False)
def create_state():
    """create the state object"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if "name" not in data:
        abort(400, description="Missing name")

    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """update the state object"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
