"""Lay out of user functions for Hello-Books API"""

from flask import Flask
from flask import Response, request, json, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_raw_jwt
import os
import datetime
import re
import random


from . import auth

from ..models import UsersTable, BookHistory, ActiveTokens, RevokedTokens
from app.decorators import jwt_required, admin_required



def validate_email(usermail):
    # import pdb; pdb.set_trace()
    valid_email = re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$)", usermail.strip())
    if not valid_email:
        return False
    return True

def validate_password(password):
    valid_password = re.match("[A-Za-z0-9@#$%^&+=]{5,}", password.strip())
    if not valid_password:
           return False
    return True


@auth.route('/register', methods=['POST'])
def register_new_user():
    """ Endpoint to register a new user"""
    if request.method == "POST":
        name = request.json.get('name')
        email = request.json.get('email')
        password = request.json.get('password')
        is_admin = request.json.get('is_admin')

    if not name or name.strip() == "":
            return Response(json.dumps({'message': 'Invalid Entry!Enter a name'}),
             content_type='application/json')
    if not email or not validate_email(email):
            return Response(json.dumps({'message': 'Invalid Entry!Enter a vaild email address'}),
             content_type='application/json')
    if not password or not validate_password(password):
            return Response(json.dumps({'message': 'Invalid Entry! Enter a vaild password'}),
             content_type='application/json')

    
    """Ensure this user is not already registered"""
    check_user = UsersTable.query.filter_by(usermail=email).first()
    print(check_user)
    if not check_user:
        hashed_password = generate_password_hash(password)
        registering_user = UsersTable(username=name, password_hash=hashed_password, usermail=email)
            

        if is_admin:
            """Let's check if this user has an admin role"""
            registering_user.is_admin = True
            registering_user.save()

            # #Automatic log in for registering admin:
            # access_token = create_access_token(identity=email)
            # ActiveTokens(email, access_token).save_token()
            return jsonify({'Message': 'New admin successful registration and Login'}),201
            # 'access_token': access_token}), 

        else:
            registering_user.save()
            # #Automatic log in for registering user
            # access_token = create_access_token(identity=email)
            # ActiveTokens(email, access_token).save_token()
            return jsonify({'Message': 'New user successful registration and Login'}),201
            # 'access_token': access_token}), 201
    return Response(json.dumps({'message': 'This email {} is already registered'. format(email)}), status=409,
    content_type='application/json')

@auth.route('/register', methods = ['PUT', 'GET'])
@jwt_required
@admin_required
def upgrade_user_to_admin():
    """Upgrade regular user to admin role"""
    if request.method == ['PUT']:
        email = request.json.get('email')
        is_admin = request.json.get('is_admin')
        if not email or not validate_email(email):
            return Response(json.dumps({'message':'Enter a valid email address'}),400,
             content_type='application/json')
        if not is_admin or is_admin =="":
            return Response(json.dumps({'message':'Enter an admin status'}),400,
             content_type='application/json')
        
        # Get  user upgrading from the db
        user_upgrading = UsersTable.retrieve_user_by_email(email)
        if user_upgrading:
            if user_upgrading.is_admin is True:
               return Response(json.dumps({'message':'you already have an admin status'}),
                 400, content_type='application/json')
            elif user_upgrading.is_admin is False:
                user_upgrading.is_admin=True
                user_upgrading.save
                return Response(json.dumps({'message':'user status successfully upgraded'}),
                 200, content_type='application/json')
        return Response (json.dumps({'message':'No user registered with this address'}), 
        status = 204, content_type='application/json' )
    elif request.method == ['GET']:
        return jsonify(users = [user.serialize for user in UsersTable.query.all()])
        

@auth.route('/login', methods=['POST'])
def login():
    """Let's define the login endpoint"""
    usermail = request.json.get('email')
    password = request.json.get('password')

    if not usermail or not validate_email(usermail):
        return Response(json.dumps({'message': 'Please enter a valid email address'}),
        status=400, content_type='application/json')
    if not password or not validate_password(password): 
        return Response(json.dumps({'message': 'Password Invalid. Please try again'}),
         status=400, content_type='application/json')
    logging_in_user = UsersTable.retrieve_user_by_email(usermail=usermail)
    logged_in_user = ActiveTokens.find_user_with_issued_token(usermail)

    # if logged_in_user.access_token is not logged_in_user.token_is_expired():
    #     return Response(json.dumps({"Token":logged_in_user.access_token,
    #      "Message:":"You are already logged in!"}), status=202, content_type='application/json')  
    
    if logged_in_user:
        access_token = create_access_token(identity=usermail)
        logged_in_user.access_token = access_token
        logged_in_user.save_issued_token()
        return Response(json.dumps({"Token":logged_in_user.access_token,
         "Message:":"Token expired.Use this new token"}),status=200, content_type='application/json')
       
    else:
        #Fetch a logging in user from the db using their email
        if logging_in_user and logging_in_user.verify_password(password):
           access_token = create_access_token(identity=usermail)
           ActiveTokens(usermail, access_token).save_issued_token()
           return jsonify({'Message': 'Login successful',
                            'access_token': access_token}), 200
        else:
           return Response(json.dumps({'Messsage': 'Unsuccessful login. Invalid email or password'}),
           status=401, content_type='application/json')

    
@auth.route('/logout', methods=['POST'])
@jwt_required
def logout():
    """Endpoint for user logout"""
    jti = get_raw_jwt()['jti']
    logged_in_user = get_jwt_identity()
    logout_token = RevokedTokens(jti=jti)
    if not RevokedTokens.is_jti_blacklisted(jti):
        logout_token.token_revoke()
        ActiveTokens.find_user_with_issued_token(user_usermail=logged_in_user).delete_active_token()
        return Response(json.dumps({'message': 'You are successfully logged out'}), status=200)
    else:
        return jsonify(
            {'message': '{} is not logged in or the token has been blacklisted'.format(logged_in_user)})


@auth.route('/reset-password', methods=['POST'])
def password_reset():
    usermail = request.json.get('email')
    password = request.json.get('password')
    
    if not usermail or not validate_email(usermail):
        # import pdb; pdb.set_trace()
        return Response(json.dumps({'message': 'Please enter a valid email address to reset your password'}),
         status=400, content_type='application/json')
    if not password or not validate_password(password):
                return Response(json.dumps({'message':'Please enter a valid password. It should combine \
                 uppercase and lowercase letters as well as include number(s)'}), 
                 content_type='application/json')
    
    user_resetting_password = UsersTable.retrieve_user_by_email(usermail=usermail)
    if not user_resetting_password:
                return Response(json.dumps({'message': 'No user is registered with this address {}'.format(usermail)}),
                status=400, content_type='application/json')
    elif user_resetting_password==password:
                return Response(json.dumps({'message': 'Please use a password that you have not used before'}), 
                status=400,content_type='application/json')
    else:
        user_resetting_password.hash_user_password(password)
        user_resetting_password.save()
        return Response(json.dumps({'message':'{}, successful password reset'.format(usermail)}), 
        status = 200, content_type='application/json')
