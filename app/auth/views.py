"""Lay out of user functions for Hello-Books API"""

from flask import Flask
from flask import Response, request, json, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity, get_raw_jwt)
from flask_mail import Message
import os
import datetime
import re
import random


from . import auth

from ..models import UsersTable, BookHistory, ActiveTokens, RevokedTokens
from app.decorators import jwt_required, admin_required
from app import mail
from app.email_token import generate_reset_password_token, confirm_reset_password_token, send_email

temp =[]

def validate_email(usermail):
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


@auth.route('/register', methods=['POST'])
def register_new_user():
    """ Endpoint to register a new user"""
    if request.method == "POST":
        name = request.json.get('name')
        email = request.json.get('email')
        password = request.json.get('password')
        confirm_password = request.json.get("confirm password")
        if confirm_password != password:
            return Response(json.dumps({'message': 'Passwords did not match'}),
            content_type='application/json')
        if not name or name.strip() == "":
            return Response(json.dumps({'message': 'Invalid Entry!Enter a name'}),
            content_type='application/json')
        if not email or not validate_email(email):
            return Response(json.dumps({'message': 'Invalid Entry!Enter a valid email address'}),
            content_type='application/json')
        if not password or not validate_password(password):
            return Response(json.dumps({'message': 'Invalid Entry! Enter a valid password'}),
            content_type='application/json')

    
    """Ensure this user is not already registered"""
    check_user = UsersTable.query.filter_by(usermail=email).first()
    
    if not check_user:
        hashed_password = generate_password_hash(password)
        registering_user = UsersTable(username=name, password_hash=hashed_password, usermail=email)
        registering_user.save()
       
        return jsonify({'Message': 'New user successful registration'}), 201
    return jsonify({'message': 'This email {} is already registered'. format(email)}), 409

@auth.route('/register', methods = ['PUT', 'GET'])
@jwt_required
@admin_required
def upgrade_user_to_admin():
    """Upgrade regular user to admin role"""
    if request.method == 'PUT':
        email = request.json.get('email')
    
        if not validate_email(email):
            return Response(json.dumps({'message':'Enter a valid email address'}),400,
                content_type='application/json')

        # Get  user upgrading from the db
        user_upgrading = UsersTable.retrieve_user_by_email(email)
        if user_upgrading:
            if user_upgrading.is_admin is False:
                user_upgrading.is_admin=True
                user_upgrading.save()
                return Response(json.dumps({'message':'user status successfully set to admin'}),
                 200, content_type='application/json')
            if user_upgrading.is_admin is True:
                user_upgrading.is_admin=False
                user_upgrading.save()
                return Response(json.dumps({'message':'user status successfully set to non-admin'}),
                 200, content_type='application/json')
        return Response (json.dumps({'message':'No user registered with this address'}), 
        status = 200, content_type='application/json' )
    if request.method == 'GET':
        all_users = UsersTable.query.paginate()
        users = all_users.items
        current_page = all_users.page
        all_pages = all_users.pages
        next_page = all_users.next_num
        prev_page = all_users.prev_num
        if not all_users:
            return Response(json.dumps({'message':'No current users' }), 404,
             content_type= 'application/json')
        library_users=[item.serialize for item in users]
        return jsonify({'library_users': library_users, "current_page": current_page, "all_pages": all_pages, 
        "next_page": next_page, "previous_page": prev_page}), 200
   
        

@auth.route('/login', methods=['POST'])
def login():
    """Let's define the login endpoint"""
    usermail = request.json.get('email')
    password = request.json.get('password')

    if not usermail:
        return Response(json.dumps({'message': 'Please enter a valid email address'}),
        status=400, content_type='application/json')
    if not password: 
        return Response(json.dumps({'message': 'Password Invalid. Please try again'}),
         status=400, content_type='application/json')
    logging_in_user = UsersTable.retrieve_user_by_email(usermail=usermail)
    logged_in_user = ActiveTokens.find_user_with_issued_token(usermail)

    if logged_in_user and not logged_in_user.token_is_expired() and logging_in_user.verify_password(password):
        access_token = create_access_token(identity=usermail)
        logged_in_user.access_token = access_token
        logged_in_user.save_issued_token()
        return Response(json.dumps({"Token":logged_in_user.access_token,
        "Message:":"You are already logged in!"}), status=202, content_type='application/json')  
    
    elif logged_in_user and logged_in_user.token_is_expired() and logging_in_user.verify_password(password):
        access_token = create_access_token(identity=usermail)
        logged_in_user.access_token = access_token
        logged_in_user.save_issued_token()
        return Response(json.dumps({"Token":logged_in_user.access_token,
         "Message":"Token expired.Use this new token"}),status=200, content_type='application/json')
    
    else:
        #Fetch a logging in user from the db using their email
        if logging_in_user and logging_in_user.verify_password(password):
           access_token = create_access_token(identity=usermail)
           ActiveTokens(usermail, access_token).save_issued_token()
           return jsonify({'Message': 'Login successful',
                            'Token': access_token}), 200

    return Response(json.dumps({'Message': 
    'Unsuccessful login. Wrong email or password'}), status=401, content_type='application/json')

    
@auth.route('/logout', methods=['POST'])
@jwt_required
def logout():
    """This method allows a user to logout"""
    email = request.json.get('email')
    if not email or not validate_email(email):
            return Response(json.dumps({'message': 'Invalid Entry!Enter a valid email address'}),
            content_type='application/json')
    else:
        jti = get_raw_jwt()['jti']
        logged_in_user = get_jwt_identity()
        if logged_in_user == email and not RevokedTokens.is_jti_blacklisted(jti):
            logout_token = RevokedTokens(jti=jti)
            logout_token.token_revoke()
            ActiveTokens.find_user_with_issued_token(email).delete_active_token()
            return Response(json.dumps({'message': 'You are successfully logged out'}),
            status=200, content_type='application/json')
        else:
            return Response(json.dumps({
                'message': '{} is not logged in or the token has been blacklisted'.format(email)}),
                status=401, content_type='application/json')



@auth.route('/reset-password', methods=['POST'])
def password_reset():
    """Endpoint for a to reset their password"""
    usermail = request.json.get('email')
    password = request.json.get('password')
    confirm_password = request.json.get("confirm password")

    token = request.args.get('token')
    if not usermail or not validate_email(usermail):
        return Response(json.dumps({'Message': 'Enter valid email to reset password'}),
        content_type='application/json'), 400
    # Check if there is a user to with the email in db.
    user_resetting_password = UsersTable.retrieve_user_by_email(usermail)
    if not user_resetting_password:
        return Response(json.dumps({
            'Message': 'No user with {} as their email. Please ensure you are registered to continue'
            .format(usermail)}), content_type='application/json'), 400
    else:
        if token:
            token_email = confirm_reset_password_token(token)
            print(token_email , user_resetting_password.usermail)
            if token_email == user_resetting_password.usermail:
                if not password or not validate_password(password):
                    return Response(json.dumps({'Message': 'Invalid Entry! Enter a valid password'}),
                    content_type='application/json'), 422
                else:
                    if confirm_password != password:
                        return Response(json.dumps({'Message': 'Passwords did not match'}),
                        content_type='application/json'), 403
                    user_resetting_password.hash_user_password(password)
                    user_resetting_password.save()
                    return Response(json.dumps({'Message': 'You have successfully reset your password'}),
                    content_type='application/json'),200
            else:
                return Response(json.dumps({'Message': 'You have issued an invalid or expired'}),
                    content_type='application/json'), 401
        else:
            # reset_url = os.getenv('front_end_url') + 'resetpassword'
            reset_url = 'SAMPLE'
            token = generate_reset_password_token(usermail)
            send_email(usermail, token, reset_url)
            return Response(json.dumps({'Message': 'A password reset link has been sent to your email'}),
                    content_type='application/json'), 200
        
        
  