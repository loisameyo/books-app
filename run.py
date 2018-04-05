from flask import Flask
#from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from app import app



# app.config['JWT_SECRET_KEY'] = 'secret-secret'
# app.config['JWT_BLACKLIST_ENABLED'] = True
# app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
# jwt = JWTManager(app)


if __name__=='__main__':
    
    app.run(debug=True)
