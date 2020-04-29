#!/usr/bin/python3
'''Flask API routes for methods'''
from flask import Flask, abort, jsonify, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_4cities(city_id):
    '''Retrieves list Cities per State'''
    city_objs = storage.get(City, city_id)
    list_places = []

    if not city_objs:
        abort(404)
    for value in city_objs.places:
        list_places.append(value.to_dict())
    return (jsonify(list_places))


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_def(place_id):
    '''Retrieves Place object'''
    placeId = storage.get(Place, place_id)
    if not placeId:
        abort(404)
    return jsonify(placeId.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''Delete a place object'''
    placed_id = storage.get(Place, place_id)
    if not placed_id:
        abort(404)
    else:
        placed_id.delete()
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def request_place4city(city_id):
    '''Request and transform HTTP to a dictionary'''
    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')

    if 'user_id' not in req:
        abort(400, 'Missing user_id')

    usr_id = storage.get(User, req['user_id'])
    if not usr_id:
        abort(404)

    if 'name' not in req:
        abort(400, 'Missing name')

    objs_id = storage.get(City, city_id)
    if not objs_id:
        abort(404)

    new_place = Place(**req)
    setattr(new_place, 'city_id', city_id)
    storage.new(new_place)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''Updates a place object'''
    place_u_id = storage.get(Place, place_id)
    if not place_u_id:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')
    for key, value in req.items():
        if not (key == 'id' or key == 'user_id' or key == 'city_id' or
                key == 'created_at' or key == 'updated_at'):
            setattr(place_u_id, key, value)
    storage.save()
    return make_response(jsonify(place_u_id.to_dict()), 200)
