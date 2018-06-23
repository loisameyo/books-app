import os
from flask import jsonify, request

def route_not_found(error=None):
        """This method handles a wrong endpoint."""
        return jsonify({
            'Message': '{} is not a valid url. Please check your spelling'.format(request.url)
        }), 404

def method_not_found(error=None):
    """This method handles an unallowed endpoint."""
    return jsonify({
            'Message': 'This method {} is not allowed on this endpoint'.format(request.method)}), 405


def internal_server_error(error=None):

    """This method handles an internal server error"""
    return jsonify({
            'message': 'Failed - Internal server error'}), 500