#!/usr/bin/python3
'''Flask API routes for methods'''
from flask import Flask, abort, jsonify, request, make_response
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def review_4place(place_id):
    '''Retrieves reviews per Place'''
    pls_objs = storage.get(Place, place_id)
    list_reviews = []

    if not pls_objs:
        abort(404)
    for value in pls_objs.reviews:
        list_reviews.append(value.to_dict())
    return (jsonify(list_reviews))


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_def(review_id):
    '''Retrieves review object'''
    reviwId = storage.get(Review, review_id)
    if not reviewId:
        abort(404)
    return jsonify(reviewId.to_dict())


@app_views.route('/review/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    '''Delete a city object'''
    reviewd_id = storage.get(Review, review_id)
    if not reviewd_id:
        abort(404)
    else:
        reviewd_id.delete()
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def request_review4place(place_id):
    '''Request and transform HTTP to a dictionary'''
    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')
    if 'user_id' not in req:
        abort(400, 'Missing user_id')
    if 'text' not in req:
        abort(400, 'Missing text')
    objsr = storage.get(User, req['user_id'])
    if not objsr:
        abort(404)
    objs_id = storage.get(Place, place_id)
    if not objs_id:
        abort(404)
    new_review = Review(**req)
    setattr(new_review, 'place_id', place_id)
    storage.new(new_review)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''Updates a review object'''
    review_u_id = storage.get(Review, review_id)
    if not review_u_id:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')
    for key, value in req.items():
        if not (key == 'id' or key == 'user_id' or key == 'place_id' or
                key == 'created_at' or key == 'updated_at'):
            setattr(review_u_id, key, value)
    storage.save()
    return make_response(jsonify(review_u_id.to_dict()), 200)
