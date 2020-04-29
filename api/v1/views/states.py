#!/usr/bin/python3
from flask import Flask, make_response, abort, jsonify, request
from models import storage
from models.state import State
from api.v1.views import app_views
import os


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def list_all():
    '''List all State object'''
    com_objs = storage.all(State).values()
    list_val = []
    for value in com_objs:
        list_val.append(value.to_dict())
    return (jsonify(list_val))


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def linked_id(state_id):
    '''Retrieves State object that are id linked'''
    objs_id = storage.get(State, state_id)
    if not objs_id:
        abort(404)
    return (jsonify(objs_id.to_dict()))


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    '''Delete a state object'''
    objsd_id = storage.get(State, state_id)
    if not objsd_id:
        abort(404)
    else:
        objsd_id.delete()
        storage.save()
        return (jsonify({}), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def request_state():
    '''Request and transform HTTP to a dictionary'''
    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')
    if 'name' not in req:
        abort(400, 'Missing name')
    new_sta = State(**req)
    new_sta.save()
    return (jsonify(new_sta.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    '''Updates a state object'''
    objs_id = storage.get(State, state_id)
    if not objs_id:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')
    for key, value in req.items():
        if not (key == 'id' or key == 'created_at' or key == 'update_at'):
            setattr(objs_id, key, value)
    storage.save()
    return (jsonify(objs_id.to_dict()), 200)
