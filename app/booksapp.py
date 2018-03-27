from flask import Flask, request, Response, json

booksapp = Flask (__name__)
class books:
  def __init__(self,book_id, book_title, book_author, book_available):
    self.book_id = book_id
    self.book_title = book_title
    self.book_author = book_author
    self.book_available = book_available
    self.allbooks = []

#when creating(post), save book as an object of the class as so
@app.route('/api/books', methods=['POST', 'GET'])
def create(self, book_id, book_title, book_author, book_available):
    if request.method == 'POST':
        books.book_title = request.form["name"]
    current_count = len(books)
    self.allBooks.append(book)
    return Response(json.dumps({'message': 'Successfully posted!'}), status=201)
    if request.method == 'GET':
        book=self.allBooks
        print (book.__dir__) 
        return Response(json.dumps(status=200)


@app.route('/api/books/<book_id>', methods=['GET', 'DELETE', 'PUT'])
def retrieve(self, book_id, book_title, book_author, book_available):
    """This method accesses a book and performs an operation to it depending on the request method"""
         book.book_id = Books(book_title, book_author, book_available)
if request.method == 'GET':
    try:
        print("retrieved book", book)
        return Response(json.dumps({'book': book}), status=200)
    except KeyError:
        return Response(json.dumps({'message': 'Invalid book Id'}), status=404)
if request.method == 'PUT':
    new_book_name = request.form['name']
    book_status = request.form['borrowed']
    try:
        book = self.allBooks()
        if book:
            self.book_name = new_book_name
            return Response(json.dumps({'message':'Updated Successfully'}), status=200)
        else:
            return Response(json.dumps({'message': 'Invalid book Id'}), status=404) 
    except KeyError:
        return Response(json.dumps({'message': 'Invalid book Id'}), status=404)
if request.method =='DELETE':
    try:
        book = Books(book_title, book_author, book_available)
        if book:
            self.allBooks.delete(book)
            return Response(json.dumps({'message':'Deleted Successfully'}), status=204)
        else:
            return Response(json.dumps({'message': 'Invalid book Id'}), status=404) 
    except KeyError:
        return Response(json.dumps({'message': 'Invalid book Id'}), status=404)'


class Users:
    def __init__(self, user_id, user_name, user_password):
    self.user_id = user_id
    self.user_name = user_name
    self.user_password = user_password
    self.allUsers = []

@app.route('/api/auth/register', methods=['POST']):
def register_user():
    return '<h1> Sign Up </h1>'
    if request.method == 'POST':
    users.user_name = request.form["username"]
    password = request.form["password"]
    return Response(json.dumps({'message': 'User registration successful!'}), status=201)'

    @app.route('/api/auth/login', methods=['POST']):
    def login_user():
        return '<h1> Please login to use library resources</h1>'
        request.authorization.username
        request.authorization.password
        if request.authorization and request.authorization.username == 'user_name' and request.authorization.password =='password':
            return '<h1> You are already logged in </h1>'



if __name__=='__main__':
app.run()

