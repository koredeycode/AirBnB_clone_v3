#!/usr/bin/python3
"""The module for the place_review views"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.place import Place
from models.review import Review
from models import storage


@app_views.route("/places/<string:id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(id=None):
    """return info about a place review objects"""
    place = storage.get(Place, id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]

    return make_response(jsonify(reviews), 200)


@app_views.route("/reviews/<string:id>", methods=['GET'], strict_slashes=False)
def get_review(id):
    """return info about a review object"""
    review = storage.get(Review, id)
    if not review:
        abort(404)
    return make_response(jsonify(review.to_dict()), 200)


@app_views.route("/reviews/<string:id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(id=None):
    """delete a review object"""
    review = storage.get(Review, id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<string:id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(id=None):
    """create a review object"""
    place = storage.get(Place, id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    if "user_id" not in data:
        abort(400, description="Missing user_id")
    if not storage.get(User, data["user_id"]):
        abort(404)
    if "text" not in data:
        abort(400, description="Missing text")

    review = Review(**data)
    review.place_id = place.id
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<string:id>", methods=['PUT'], strict_slashes=False)
def update_review(id=None):
    """update the review object"""
    review = storage.get(Review, id)

    if not review:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
