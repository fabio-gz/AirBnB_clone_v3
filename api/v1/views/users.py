#!/usr/bin/python3
'''Flask API routes for methods'''
from flask import Flask, abort, jsonify, request, make_response
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_users():
    '''List all Users objects'''
    us_objs = storage.all(User).values()
    list_us = []
    for value in us_objs:
        list_us.append(value.to_dict())
    return (jsonify(list_us))


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def lin_user_id(user_id):
    '''Retrieves User object that are id linked'''
    usr_id = storage.get(User, user_id)
    if not usr_id:
        abort(404)
    return (jsonify(usr_id.to_dict()))


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    '''Delete a user object'''
    usrd_id = storage.get(User, user_id)
    if not usrd_id:
        abort(404)
    else:
        usrd_id.delete()
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def request_user():
    '''Request and transform HTTP to a dictionary'''
    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')
    if 'email' not in req:
        abort(400, 'Missing email')
    if 'password' not in req:
        abort(400, 'Missing password')
    new_usr = User(**req)
    new_usr.save()
    return make_response(jsonify(new_usr.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''Updates a user object'''
    usr_id = storage.get(User, user_id)
    if not usr_id:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, 'Not a JSON')
    for key, value in req.items():
        if not (key == 'id' or key == 'created_at' or
                key == 'updated_at' or key == 'email'):
            setattr(usr_id, key, value)
    storage.save()
    return make_response(jsonify(usr_id.to_dict()), 200)
