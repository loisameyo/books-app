"""Decorators to be used in the books_api endpoints"""
from flask import Response, json
from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt
from functools import wraps
from app.models import UsersTable, RevokedTokens


def admin_required(func):
    """Verify that a user is admin and has valid token 
        to perform admin functions"""

    @wraps (func)
    def validate_admin_and_token(*args, **kwargs):
        jti = get_raw_jwt() ['jti']
        logged_in_usermail = get_jwt_identity()
        logged_in_user = UsersTable.retrieve_user_by_email(logged_in_usermail)
        if RevokedTokens.is_jti_blacklisted(jti):
            return Response(json.dumps({'message':'This token is blacklisted'}), 
            status = 401 , content_type = 'application/json')
        if not logged_in_user.is_admin:
            return Response(json.dumps({
                'message':'Unauthorized. You need to be an admin to perform this function'}), 
            status = 401 , content_type = 'application/json')
        return func(*args, **kwargs)
    return validate_admin_and_token

