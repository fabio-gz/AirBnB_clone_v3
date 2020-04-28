#!/usr/bin/python3
'''Indicate the route for flask access'''
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    '''Status indicator'''
    return (jsonify({'status': 'OK'}))


@app_views.route('/stats', strict_slashes=False)
def objects_status():
    '''retrieve numbers of each object'''
    obj_status = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return (jsonify(obj_status))
