"""Lay out of user functions for Hello-Books API"""
from flask import Flask
from flask import Response, request, json, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_raw_jwt
import os
import datetime
import re
import random


from app import app

from ..models import UsersTable, BookHistory, ActiveTokens, RevokedTokens



def validate_email(usermail):
    print("xyz")
    # import pdb; pdb.set_trace()
    valid_email = re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", usermail.strip())
    if not valid_email:
        return False
    return True

def validate_password(password):
    valid_password = re.match("[A-Za-z0-9@#$%^&+=]{5,}", password.strip())
    if not valid_password:
           return False
    return True


@app.route('/api/v2/auth/register', methods=['POST'])
def register_new_user():
    if request.method == "POST":
        name = request.json.get('name')
        email = request.json.get('email')
        passwd = request.json.get('passwd')
        is_admin = request.json.get('is_admin')

    if not email or not validate_email(email):
            return Response(json.dumps({'message': 'Invalid Entry!Enter a vaild email address'}), content_type='application/json')
    if not passwd or not validate_password(passwd):
            return Response(json.dumps({'message': 'Invalid Entry!Enter a vaild password'}), content_type='application/json')

    check_username = UsersTable.verify_username(name)
    if check_username == False:
            return Response(json.dumps({'message': 'Access denied. Use a different username'}), status = 403)

    check_user = UsersTable.query.filter_by(usermail=email).first()
    """Let's ensure that this user is not already a registered user in the database"""
    if not check_user:
        hashed_passwd = generate_password_hash(passwd)
        registering_user = UsersTable(username=name, passwd_hash=hashed_passwd, usermail=email)
            

        if is_admin:
            """Let's check if this user has an admin role"""
            registering_user.is_Admin = True
            registering_user.save()
            return Response(json.dumps({'message': 'New user successfully regsitered as an admin'}), status=201)
        else:
            registering_user.save()
            return Response(json.dumps({'message': 'Successfully registered as a new user (non-admin)'}), status=201)
    return Response(json.dumps({'message': ' Not allowed:  This email address is already registered'}), status=403)


@app.route('/api/v2/auth/login', methods=['POST'])
def login():
    """Let's define the login endpoint"""
    usermail = request.json.get('email')
    passwd = request.json.get('passwd')
    if not usermail or not validate_email(usermail):
        return Response(json.dumps({'message': 'Please enter a valid email address'}), content_type='application/json')
    if not passwd or not validate_password(passwd): 
        return Response(json.dumps({'message': 'Password Invalid. Please try again'}), content_type='application/json')
    logging_in_user = UsersTable.retrieve_user_by_email(usermail=usermail)
    if check_password_hash(logging_in_user.passwd_hash, passwd):
        logging_in_user.logged_in = True
        logging_in_user.save()
        token = create_access_token(identity=usermail)
        if ActiveTokens.find_user_with_issued_token(usermail) == False:
            return Response(json.dumps({'message': 'Access denied. User cannot login twice'}, status = 403, content_type='application/json'))
        ActiveTokens(user_usermail=usermail, access_token=token).save_issued_token()
        user_token=RevokedTokens(jti=token)
        user_token.save()
        return jsonify({"Token":token,"Success:":"Login Successful"})

    return jsonify({"message":"Unsuccessful login. Passwords do not match"}), 403
        

    
@app.route('/api/v2/auth/logout', methods=['POST'])
@jwt_required
def logout():
    """Endpoint for user logout"""
    jti = get_raw_jwt()['jti']
    logged_in_user = get_jwt_identity()
    logout_token = RevokedTokens(jti=jti)
    if not RevokedTokens.is_jti_blacklisted(jti):
        logout_token.token_revoke()
        ActiveTokens.get_access_token(user_usermail=logged_in_user).delete_active_token()
        return Response(json.dumps({'message': 'You are successfully logged out'}), status=200)
    else:
        return jsonify(
            {'message': '{} is not logged in or the token has been blacklisted'.format(logged_in_user)})


@app.route('/api/v2/auth/reset-password', methods=['POST'])
def password_reset():
    usermail = request.json.get('usermail')
    password = request.json.get('password')
    
    if not usermail or usermail.strip()== " " or not validate_email(usermail):
        # import pdb; pdb.set_trace()
        return Response(json.dumps({'message': 'Please enter a valid email address to reset your password'}), content_type='application/json')
    if not password or not validate_password(password):
                return Response(json.dumps({'message':\
                'Please enter a valid password. It should combine uppercase and lowercase letters as well as include number(s)' }), content_type='application/json')
    
    user_resetting_password = UsersTable.retrieve_user_by_email(usermail=usermail)
    if not user_resetting_password:
                return Response(json.dumps({'message': 'No user is registered with this address {}'.format(usermail)}), content_type='application/json')
    elif user_resetting_password==password:
                return Response(json.dumps({'message': 'Please use a password that you have not used before'}), content_type='application/json')
    else:
        user_resetting_password.hash_user_passwd(password)
        user_resetting_password.save()
        return Response(json.dumps({'message': '{}, you have successfully reset your password'.format(usermail)}), status = 200, content_type='application/json')
