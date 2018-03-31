from flask import Flask, request, Response, json, session
#from models import User

def create_app():
    app = Flask (__name__)

    books = {}
    users = []

    @app.route('/api/v1/books', methods=['POST', 'GET'])
    def save_book():
        #This method allows a user (admin) to add new books
        if request.method == 'POST':
            book_name = request.json.get('name')
            current_count = len(books)
            books[current_count + 1] = {'book_name': book_name, 'borrowed': False}
            return Response(json.dumps({'message': 'Successfully posted!'}), status=201, mimetype='application/json')
        #Any user can view all the books available:
        elif request.method == 'GET':
            retrieved_books = list(books.values())
            return Response(json.dumps({'books': retrieved_books}), status=200, mimetype='application/json')
      

    @app.route('/api/v1/books/<book_id>', methods=['GET', 'DELETE', 'PUT'])
    def access_book(book_id):
        #This method accesses a book and performs an operation to it depending on the request method
        #For instance, the request method below allows you to retrieve a particluar book
        if request.method == 'GET':
            book = books[int(book_id)]
            print("retrieved book", books[int(book_id)])
            return Response(json.dumps({'book': book}), status=200, mimetype='application/json')
        return Response(json.dumps({'message': 'Invalid book Id'}), status=404, mimetype='application/json')

        #This request method allows you to update a particluar book
        if request.method == 'PUT':
            new_book_name = request.json.get('name')
            book_status = request.json.get('name')
            book = books[int(book_id)]
            if book:
                books[int(book_id)] = {'book_name': new_book_name, 'borrowed': book_status}
                return Response(json.dumps({'message':'Updated Successfully'}), status=200, mimetype='application/json')
            else:
                return Response(json.dumps({'message': 'Invalid book Id'}), status=404, mimetype='application/json') 
            
        #This request method allows you to delete a particluar book
        if request.method=='DELETE':
            book = books[int(book_id)]
            if book:
                del books[int(book_id)]
                return Response(json.dumps({'message':'Deleted Successfully'}), status=204, mimetype='application/json')
            else:
                return Response(json.dumps({'message': 'Invalid book Id'}), status=404, mimetype='application/json') 
            
    #This method allows the user to borrow a book
    @app.route('/api/v1/users/books/<book_id>', methods=['GET'])
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
            email = request.json.get('email')
            passwd = request.json.get('passwd')
            confirm_passwd = request.json.get('confirm_passwd')
            current_users = len(users)
            users.append({'email': email,'logged_in':False}) 
            return Response(json.dumps({'message': 'User registration successful!'}), status=201, mimetype='application/json')
        else:
                return Response(json.dumps({'message': 'User registration unsuccessful!'}), status=404, mimetype='application/json')
    @app.route('/api/auth/login', methods=['POST'])
    def user_login():
        if request.method =='POST':
            user_email = request.json.get('email')
            user_passwd = request.json.get('passwd')
            if user_email == 'email' and user_passwd == 'passwd':
                session['logged_in'] = True
            else:
                flash('You have keyed in a wrong email or password!')
                return user_login() 
    @app.route('/api/auth/reset-password', methods=['POST'])
    def passwd_reset():
        user_email = request.json.get('email')
        new_passwd = request.json.get('new_passwd')
        user = users[int(user_id)]
        if user:
                users[int(user_id)] = {'email': user_email, 'new_passwd': new_passwd}
                return Response(json.dumps({'message':'Password reset successfully'}), status=200, mimetype='application/json')
        else:
                return Response(json.dumps({'message': 'User does not exist'}), status=404, mimetype='application/json') 


    @app.route('/api/auth/logout', methods=['POST'])
    def user_logout():
        session['logged_in']= False


    

    return app