from flask import request, Response, json, session, jsonify
#from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from app import app
from .models import Books, Users
books = []
users = []

@app.route('/api/v1/books', methods=['POST', 'GET'])
def add_book():
    """This method allows you to add a new book or retrieve a particular"""
    if request.method == 'POST':
        book_name = request.json.get('name')
        author = request.json.get('author')
        pub_year = request.json.get('pub_year')

        if book_name == None or book_name == "":
            return Response(json.dumps({'message': 'Invalid Entry!'}), content_type='application/json')
        if author == None or author == "":
            return Response(json.dumps({'message': 'Invalid Entry!'}), content_type='application/json')
        if pub_year == None or pub_year == "":
            return Response(json.dumps({'message': 'Invalid Entry!'}), content_type='application/json')

        for book in books:
            if book.name == book_name and book.author == author and book.year == pub_year:
                return Response(json.dumps({'message': 'This book already exists!'}), status=202, content_type='application/json')
            if book.name == book_name and book.author == author and book.year == pub_year:
                book.count += 1
                return Response(json.dumps({'message': 'This book already exists'}), status=401, content_type='application/json')

        new_book = Books(book_name, author, pub_year)
        books.append(new_book)
        return Response(json.dumps({'message': 'Successfully posted!'}), status=201, content_type='application/json')

        """A user can view all books available"""
    elif request.method == 'GET':
        if len(books) == 0:
            return Response(json.dumps({'message': 'No books available'}), status=204, content_type='application/json')
        return jsonify(book=[item.serialize for item in books])


@app.route('/api/v1/books/<book_id>', methods=['GET', 'DELETE', 'PUT'])
def access_book(book_id):
    """This method accesses a book and performs an operation to it depending on the request method"""
    """For instance, the request method below allows you to retrieve a particluar book"""
    if request.method == 'GET':
        for book in books:
            if book.id == book_id:
                return Response(json.dumps(book.serialize), status=200, content_type='application/json')
                
        return Response(json.dumps({"Message": "No book with that Id"}), status=200, content_type='application/json')
        

    """This request method allows you to update a retrieved book"""
    if request.method == 'PUT':
        for book in books:
            if book.id == book_id:
                if request.json['name'] or request.json['name'] != "":
                    new_book_name = request.json['name']
                else:
                    new_book_name = book.name
                    
                if request.json['author'] or request.json['author'] != "":
                     new_author = request.json['author']
                else:
                    new_author = book.author
           
                if request.json['pub_year'] or request.json['pub_year'] != "":
                        new_pub_year = request.json['pub_year']
                else:
                    new_pub_year = book.year

                book.name = new_book_name
                book.author = new_author
                book.pub_year = new_pub_year
                return Response(json.dumps({'message': 'Updated Successfully'}), status=200, content_type='application/json')


    """This request method allows you to delete a retrieved book"""
    if request.method == 'DELETE':
        for book in books:
            if book.id == book_id:
                print(book_id)
                books.remove(book)
            return Response(json.dumps({'message': 'Deleted Successfully'}), status=204, content_type='application/json')
        else:
            return Response(json.dumps({'message': 'Invalid book Id'}), status=404, content_type='application/json')


@app.route('/api/v1/users/books/<book_id>', methods=['POST'])
def borrow_book(book_id):
    """ This method allows a registered user to borrow a book"""
    for book in books:
        if book.id != book_id:
            return Response(json.dumps({'message': 'Book does not exist'}), status=200, content_type='application/json')
        elif book.id == book_id and book.status == True:
            book.status == False
            return Response(json.dumps({'message': 'Book successfully borrowed'}), status=200, content_type='application/json')
            break
        else:
         return Response(json.dumps({'message': 'Book is not available'}), status=200, content_type='application/json')
        

@app.route('/api/v1/auth/register', methods=['POST'])
def user_register():
    """This method allows a new user to register"""
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']


        if email== None or email == "":
            return Response(json.dumps({'message': 'Invalid Entry!'}), content_type='application/json')
        if password == None or password == "":
            return Response(json.dumps({'message': 'Invalid Entry!'}), content_type='application/json')
        
        for user in users:
            if user.email == email:
                return Response(json.dumps({'message': 'Sorry, this user already exists'}), status=401, content_type='application/json')


        new_user = Users(email, password)
        users.append(new_user)
        return jsonify(new_user.serialize)
        #Response(json.dumps({'message': 'User Registration succesful!'}), status=201, content_type='application/json')      


@app.route('/api/v1/auth/login', methods=['POST'])
def user_login():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')
        for user in users:
            if user.email == email:
                if user.password == password:
                    return Response(json.dumps({'message': 'Login Successful'}))
                    break
    return Response(json.dumps({'message': 'Login Unsuccesful. Non-existing user'}))


@app.route('/api/v1/auth/reset-password', methods=['POST'])
def passwd_reset():
    """This method allows a regist  user to reset their password"""
    if request.method == 'POST':
        user_email = request.json.get('email')
        new_password = request.json.get('new_password')
        for user in users:
            if user.email == user_email:
                break
                if user:
                    user.password = new_password
        return Response(json.dumps({'message': 'Password reset successfully'}), status=201, content_type='application/json')
        # else user does not exist


@app.route('/api/v1/auth/logout', methods=['POST'])
def user_logout():
    """This method allows a person who is logged in to log out"""
    if session.get('logged_in'):
        session['logged_in'] = False
        return Response(json.dumps({'message': 'You are logged out'}), status=201, content_type='application/json')
    else:
        return 'You are not logged in'



