#!/usr/bin/python3
"""The module for the users endpoint"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.user import User
from models import storage


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_users():
    """return info about the users objects"""
    users = storage.all(User).values()
    users = [user.to_dict() for user in users]
    return (jsonify(users))


@app_views.route("/users/<user_id>", methods=['GET'],
                 strict_slashes=False)
def get_user(user_id=None):
    """return info about a user object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return make_response(jsonify(user.to_dict()), 200)


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id=None):
    """delete a user object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users/", methods=['POST'], strict_slashes=False)
def create_user():
    """create a user object"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if "email" not in data:
        abort(400, description="Missing email")

    if "password" not in data:
        abort(400, description="Missing password")
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id=None):
    """update the user object"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
