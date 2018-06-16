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

from ..models import UsersTable, BookHistory, ActiveTokens, IssuedTokens



@app.route('/api/v2/auth/register', methods=['POST'])
def register_new_user():
    if request.method == "POST":
        name = request.json.get('name')
        email = request.json.get('email')
        passwd = request.json.get('passwd')
        is_admin = request.json.get('is_admin')

        # valid_email = re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email.strip())

        # if not valid_email:
        #     return Response(json.dumps({'message': 'Invalid Entry! Give a vaild name to register'}), content_type='application/json')
        if email == None or email == "" or email.strip()=="" :
            return Response(json.dumps({'message': 'Invalid Entry!Enter a vaild email address'}), content_type='application/json')
        if passwd == None or passwd == "" or passwd.strip()=="":
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
                return Response(json.dumps({'message': 'Successfully registered as a new user'}), status=201)
        return Response(json.dumps({'message': ' Not allowed:  This user is already registered'}), status=403)


@app.route('/api/v2/auth/login', methods=['POST'])
def login():
    """Let's define the login endpoint"""
    usermail = request.json.get('email')
    passwd = request.json.get('passwd')
    invalid_email = (not usermail or usermail == None or usermail == "" or usermail.strip()=="")
    if invalid_email:
        return Response(json.dumps({'message': 'Email Invalid. Please try again'}))
    invalid_passwd = (not passwd or passwd == None or passwd == "" or passwd.strip()=="")
    if invalid_passwd:
        return Response(json.dumps({'message': 'Password Invalid. Please try again'}))
    logging_in_user = UsersTable.retrieve_user_by_email(usermail=usermail)
    if check_password_hash(logging_in_user.passwd_hash, passwd):
        logging_in_user.logged_in = True
        logging_in_user.save()
        token = create_access_token(identity=usermail)
        if ActiveTokens.find_user_with_issued_token(usermail) == False:
            return Response(json.dumps({'message': 'Access denied. User cannot login twice'}), status = 403)
        ActiveTokens(user_usermail=usermail, access_token=token).save_issued_token()
        u=IssuedTokens(jti=token)
        u.save()
        return jsonify({"Token":token,"Success:":"Login Successful"})

    return jsonify({"message":"Unsuccessful login. Passwords do not match"}), 403
        

    
@app.route('/api/v2/auth/logout', methods=['POST'])
@jwt_required
def logout():
    """Endpoint for user logout"""
    jti = get_raw_jwt()['jti']
    logged_in_user = get_jwt_identity()
    logout_token = IssuedTokens(jti=jti)
    if not IssuedTokens.is_jti_blacklisted(jti):
        logout_token.token_revoke()
        ActiveTokens.get_access_token(user_usermail=logged_in_user).delete_active_token()
        return Response(json.dumps({'message': 'You are successfully logged out'}), status=200)
    else:
        return jsonify(
            {'message': '{} is not logged in or the token has been blacklisted'.format(logged_in_user)})


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
