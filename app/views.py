from flask import request, Response, json, session, jsonify
from app import app
from .models import Books
books = []
users = []

@app.route('/api/v1/books', methods=['POST', 'GET'])
def add_book():
    #This method allows a user (admin) to add new books
    if request.method == 'POST':
        book_id = len(books) + 1
        book_name = request.json['name']
        author = request.json['author']
        pub_year = request.json['pub_year']
        new_book= Books(book_name, author, pub_year, book_id,)
        books.append(new_book)
        return Response(json.dumps({'message': 'Successfully posted!'}), status=201, content_type='application/json')
    # Any user can view all the books available:
    elif request.method == 'GET':
        return jsonify(book= [item.serialize for item in books])
    

@app.route('/api/v1/books/<int:book_id>', methods=['GET', 'DELETE', 'PUT'])
def access_book(book_id):
    #This method accesses a book and performs an operation to it depending on the request method
    #For instance, the request method below allows you to retrieve a particluar book
    if request.method == 'GET':
        for book in books:
            if book.id == book_id:
                break
        if book.id != book_id:
            return Response(json.dumps({"Message": "No book with that Id"}), status=200, mimetype='application/json')
        else:
            return Response(json.dumps(book.serialize), status=200, mimetype='application/json')
    # return Response(json.dumps({'message': 'Invalid book Id'}), status=404, mimetype='application/json')

    #This request method allows you to update a particluar book
    if request.method == 'PUT':
        book_name = request.json['name']
        author = request.json['author']
        pub_year = request.json['pub_year']
        for book in books:
            if book.id == book_id:
                break

        if book.id == book_id:
            book.name = book_name
            book.author = author
            book.pub_year = pub_year
            return Response(json.dumps({'message':'Updated Successfully'}), status=200, mimetype='application/json')
        else:
            return Response(json.dumps({'message': 'Invalid book Id'}), status=404, mimetype='application/json')
             
        
    #This request method allows you to delete a particluar book
    if request.method=='DELETE':
        print("DELETE", books, book_id)

        book = books[int(book_id)]
        if book:
            del books[int(book_id)]
            return Response(json.dumps({'message':'Deleted Successfully'}), status=204, mimetype='application/json')
        else:
            return Response(json.dumps({'message': 'Invalid book Id'}), status=404, mimetype='application/json') 
        
#This method allows the user to borrow a book
@app.route('/api/v1/users/books/<book_id>', methods=['POST'])
def borrow_book(book_id):
    retrieved_book_info = books[int(book_id)]
    if retrieved_book_info['borrowed']:
        #Book has been borowed
        return Response(json.dumps({'message':'Book is borrowed'}), status=404, mimetype='application/json')
    else:
        #Book has not been borrowed
        retrieved_book_info['borrowed'] = True
        books[int(book_id)]= retrieved_book_info
        return Response(json.dumps({'message': 'Book issued'}), status=200, mimetype='application/json')


@app.route('/api/v1/auth/register', methods=['POST'])
#This method allows a normal user (who is not the admin) to register to use the library
def user_register():
    if request.method=='POST':
        email = request.json['email']
        passwd = request.json['passwd']
        current_users = len(users)
        users[current_users +1]=({'email': email,'passwd':passwd, 'logged_in':True}) 
        if email in [None, ""]:
            return ("Unaccepted. Please enter your email")           
        return Response(json.dumps({'message': 'User registration successful!'}), status=201, mimetype='application/json')
    else:
        return Response(json.dumps({'message': 'User registration unsuccessful!'}), status=404, mimetype='application/json')
@app.route('/api/v1/auth/login', methods=['POST'])
def user_login():
    if request.method=='POST':
        email=request.json.get('email')
        passwd=request.json.get('passwd')
        print(users)
        for user_id in users:
            user = users[user_id] 
            if user["email"]==email:
                if user["passwd"]==passwd:
                    return Response(json.dumps({'message':'Login Successful'}))
        return Response(json.dumps({'message':'Login Unsuccesful'}))
@app.route('/api/v1/auth/reset-password', methods=['POST'])
def passwd_reset():
    if request.method=='POST':
        user_email = request.json.get('email')
        new_passwd = request.json.get('new_passwd')
        for user in users:
            if user['email'] == user_email:
                break
                if user:
                    user['passwd'] = new_passwd
        return Response(json.dumps({'message':'Password reset successfully'}), status=201, mimetype='application/json')
    else:
        return Response(json.dumps({'message': 'User does not exist'}), status=404, mimetype='application/json')  

@app.route('/api/v1/auth/logout', methods=['POST'])
def user_logout():
    if session.get('logged_in'):
        session['logged_in']= False
        return Response(json.dumps({'message':'You are logged out'}),status=201, mimetype='application/json')
    else:
        return 'You are not logged in'
    