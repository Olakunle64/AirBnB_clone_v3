#!/usr/bin/python3
""" This module contains a blue print for a restful API that
    works for place objects
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from models.city import City


# @app_views.route('/states/<state_id>/cities/', methods=['GET', 'POST'])
@app_views.route(
        '/places/<place_id>/reviews',
        methods=['GET', 'POST'], strict_slashes=False
        )
def post_get_review_obj(place_id):
    """ This function contains two http method handler

        GET:
            return the all review objects related to the place_id
        POST:
            create a new place with the city_id given
        """
    if request.method == 'GET':
        place = storage.get(Place, place_id)
        review_list = []
        if place:
            for review in place.reviews:
                review_list.append(review.to_dict())
            return jsonify(review_list)
        else:
            abort(404)
    elif request.method == 'POST':
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        review_dict = request.get_json()
        if not review_dict:
            abort(400, description="Not a JSON")
        if "text" not in review_dict:
            abort(400, description="Missing text")
        if "user_id" not in review_dict:
            abort(400, description="Missing user_id")
        # user_objects = storage.get(User, review_dict["user_id"])
        # key = 'User.{}'.format(places_dict["user_id"])
        user = storage.get(User, review_dict["user_id"])
        if not user:
            abort(404)
        review_dict["place_id"] = place_id
        new_review = Review(**review_dict)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route(
        '/reviews/<review_id>',
        methods=['GET', 'DELETE', 'PUT'],
        strict_slashes=False
        )
def delete_put_get_review_obj(review_id):
    """ This function contains three http method handler

    GET:
        return the review with the respective review_id
    DELETE:
        delete the place with the respective review_id
    PUT:
        update the place with the respective review_id
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    elif request.method == 'GET':
        return jsonify(review.to_dict())
    elif request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        review_dict = request.get_json()
        if not review_dict:
            abort(400, description="Not a JSON")
        const = ["id", "user_id", "updated_at", "created_at", "place_id"]
        for key, value in review_dict.items():
            if key not in const:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
