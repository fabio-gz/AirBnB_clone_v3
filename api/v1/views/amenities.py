#!/usr/bin/python3
'''Flask API routes for methods'''
from flask import Flask, abort, jsonify, request, make_response
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_amenities():
    '''List all Amenities object'''
    ame_objs = storage.all(Amenity).values()
    list_ame = []
    for value in ame_objs:
        list_ame.append(value.to_dict())
    return (jsonify(list_ame))


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def ret_amenities(amenity_id):
    '''Retrieves Amenities object'''
    objs_ame = storage.get(Amenity, amenity_id)
    if not objs_ame:
        abort(404)
    return (jsonify(objs_ame.to_dict()))


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenities(amenity_id):
    '''Delete Amenities object'''
    objsd_ame = storage.get(Amenity, amenity_id)
    if not objsd_ame:
        abort(404)
    else:
        objsd_ame.delete()
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def request_amenity():
    '''Request and transform HTTP to a dictionary'''
    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')
    if 'name' not in req:
        abort(400, 'Missing name')
    new_ame = Amenity(**req)
    new_ame.save()
    return make_response(jsonify(new_ame.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''Updates a amenity object'''
    ameni_id = storage.get(Amenity, amenity_id)
    if not ameni_id:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')
    for key, value in req.items():
        if not (key == 'id' or key == 'created_at' or key == 'updated_at'):
            setattr(ameni_id, key, value)
    storage.save()
    return make_response(jsonify(ameni_id.to_dict()), 200)
