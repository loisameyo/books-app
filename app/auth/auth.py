"""Lay out of user functions for Hello-Books API"""
from flask import Flask
from flask import Response, request, json, jsonify, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_raw_jwt
from werkzeug.security import generate_password_hash, check_password_hash

import re
import random


from app import app
from . import auth
from app.models import UsersTable, UserHistory, ActiveTokens, IssuedTokens


@app.route('/api/v2/au:th/register', methods=['POST'])
def register_new_user():
    if request.method == "POST":
        name = request.json.get('name')
        email = request.json.get('email')
        passwd = request.json.get('passwd')
        is_admin = request.json.get('is_admin')

        valid_email = re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email.strip())

        if not valid_email:
            return Response(json.dumps({'message': 'Invalid Entry! Give a vaild name to register'}), content_type='application/json')
        if email == None or email == "" or email.strip()!="" :
            return Response(json.dumps({'message': 'Invalid Entry!Enter a vaild email address'}), content_type='application/json')
        if passwd == None or passwd == "" or passwd.strip()!="":
            return Response(json.dumps({'message': 'Invalid Entry!Enter a vaild password'}), content_type='application/json')

        check_user = UsersTable.query.filter_by(usermail=email).first()

        """Let's ensure that this user is not already a registered user in the database"""
        if not check_user:
            hashed_passwd = generate_password_hash(passwd)
            registering_user = UsersTable(user_id=random.randint(1111,9999), username=name, passwd_hash=hashed_passwd, usermail=email)
            # registering_user.hash_user_passwd(passwd)

            if is_admin:
                """Let's check if this user has an admin role"""
                registering_user.is_Admin = True
                registering_user.save()
                return Response(json.dumps({'message': 'New user successfully regsitered as an admin'}), status=201)
            else:
                registering_user.save()
                return Response(json.dumps({'message': 'Successfully registered as a new user'}), status=201)
        return Response(json.dumps({'message': ' Not allowed:  This user is already registered'}), status=200)


@app.route('/api/v2/auth/login', methods=['POST'])
def login():
    """Let's define the login endpoint"""
    usermail = request.json.get('email')
    passwd = request.json.get('passwd')
    invalid_email = (not usermail or usermail == None or usermail == "" or usermail.strip()!="")
    if invalid_email:
        return Response(json.dumps({'message': 'Email Invalid. Please try again'}))
    invalid_passwd = (not passwd or passwd == None or passwd == "" or passwd.strip()!="")
    if invalid_passwd:
        return Response(json.dumps({'message': 'Password Invalid. Please try again'}))
    logging_in_user = UsersTable.get_user_by_email(usermail)
    """Let's check if this user is already logged in"""
    logged_in_user = ActiveTokens.find_user_with_token(usermail)
    if logged_in_user and not logged_in_user.is_expired() and logging_in_user.check_password(passwd):
        return Response(json.dumps({'message': 'You are already logged in.', 'Access token': logged_in_user.access_token}), status=200)
    elif logged_in_user and logged_in_user.is_expired():
        access_token = create_access_token(identity=usermail)
        logged_in_user.access_token = access_token
        logged_in_user.save_token()
    else:
        """Fetch user from the db"""
        if logging_in_user and logging_in_user.check_password(passwd):
            access_token = create_access_token(identity=usermail)
            ActiveTokens(usermail, access_token).save_token()
            return Response(json.dumps({'message': 'You are successfully logged in.', 'Access token': access_token}), status=201)
        else:
            return Response(json.dumps({'message': 'Incorrect email or password. Try again'}), status=401)


@app.route('/api/v2/auh/logout', methods=['POST'])
@jwt_required
def logout():
    """Let's log a user out!"""
    usermail = request.json.get('email')
    if usermail == None or usermail == "" or usermail.strip()!="":
        return Response(json.dumps({'message': 'Enter a valid email to logout'}))
    else:
        logging_out_user = UsersTable.get_user_by_email(usermail)
        if not logging_out_user:
                return Response(json.dumps({'message': 'Unallowed. This user {} is not registered'.format(usermail)}))
        else:
            jti = get_raw_jwt()['jti']
            logged_in_user = get_jwt_identity()
            if logged_in_user == usermail and not IssuedTokens.is_jti_blacklisted(jti):
                revoke_token = IssuedTokens(jti=jti)
                revoke_token.revoke()
                ActiveTokens.find_user_with_token(usermail).delete_active_token()
                return Response(json.dumps({'message': 'You are successfully logged out'}), status=200)
            else:
                jsonify(
                    {'message': '{} is not logged in or the token has been blacklisted'.format(usermail)})


@app.route('/api/v2/auth/reset-password', methods=['POST'])
def password_reset():
    email = request.json.get('email')
    password = request.json.get('password')
    confirm_password =request.json.get('password2')
    if confirm_password != password:
        return Response(json.dumps({'message': 'Your password entry does not match'}))
    if email == None or email == "" or email.strip()!="":
        return Response(json.dumps({'message': 'Please enter your email to reset your password'}))
    if password == None or password == "":
                return Response(json.dumps({'message': 'Please enter your new password'}))
    else:
        updated_password = UsersTable.get_user_by_email(email)
        if not updated_password:
                return Response(json.dumps({'message': 'No user is registered with this address {}'.format(email)}))
        elif updated_password.check_password(password):
                return Response(json.dumps({'message': 'Please use a password that you have not used before'}))
        else:
            updated_password.hash_password(password)
            updated_password.save()
            return Response(json.dumps({'message': 'Password reset successful'}))
