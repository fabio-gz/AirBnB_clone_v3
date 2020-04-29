#!/usr/bin/python3
'''Flask API routes for methods'''
from flask import Flask, abort, jsonify, request, make_response
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_4state(state_id):
    '''Retrieves list Cities per State'''
    sta_objs = storage.get(State, state_id)
    list_cities = []

    if not sta_objs:
        abort(404)
    for value in sta_objs.cities:
        list_cities.append(value.to_dict())
    return (jsonify(list_cities))


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_def(city_id):
    '''Retrieves City object'''
    cityId = storage.get(City, city_id)
    if not cityId:
        abort(404)
    return jsonify(cityId.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    '''Delete a city object'''
    cityd_id = storage.get(City, city_id)
    if not cityd_id:
        abort(404)
    else:
        cityd_id.delete()
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def request_city4state(state_id):
    '''Request and transform HTTP to a dictionary'''
    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')
    if 'name' not in req:
        abort(400, 'Missing name')
    objs_id = storage.get(State, state_id)
    if not objs_id:
        abort(404)
    new_city = City(**req)
    setattr(new_city, 'state_id', state_id)
    storage.new(new_city)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''Updates a city object'''
    city_u_id = storage.get(City, city_id)
    if not city_u_id:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')
    for key, value in req.items():
        if not (key == 'id' or key == 'created_at' or key == 'updated_at'):
            setattr(city_u_id, key, value)
    storage.save()
    return make_response(jsonify(city_u_id.to_dict()), 200)
