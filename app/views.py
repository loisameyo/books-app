from flask import Flask
from flask import Response, request, json, jsonify, abort
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_raw_jwt


from app import app
from .models import UsersTable, Library, BookHistory, ActiveTokens, IssuedTokens


@app.route('/api/v2/books', methods=['POST'])
def post_book():
    """This method allows a user to add a new book"""
    if request.method == "POST":
        title = request.json.get('title')
        author = request.json.get('author')
        year = request.json.get('year')
        new_book = Library(
            book_title=title, book_author=author, publication_year=year)
        new_book.save_book_to_db()
        return Response(json.dumps({'message': 'You have successfully added the book {} by {} the year {}'.format(title, author, year)}), status=200)        


@app.route('/api/v2/books', methods = ['GET'])
def retrieve_all_books():
    """Let's find out all the books in the library"""
    if request.method =="GET":
        all_books = Library.query.all()
        if not all_books:
            return Response(json.dumps({'message': 'No books available in the Library'}), status=200)
        return jsonify(books=[item.serialize for item in all_books]), 200



@app.route('/api/v2/books/<book_id>', methods = ['GET'])
def retrieve_particular_book(book_id):
    """This method allows us to retrieve a particular book"""
    try:
        required_book_id = int(book_id)
        retrieved_book = Library.query.filter_by(
            book_id=required_book_id).first()
        if not retrieved_book:
            return Response(json.dumps({'Message': 'There is no book with that ID in the Library'}), status=200)
        else:
            return jsonify(retrieved_book.serialize)
    except ValueError:
        return Response(json.dumps({'Message': 'Please enter a valid book ID'}), status=404)


@app.route('/api/v2/books/<bookId>', methods=['PUT', 'DELETE'])
#@jwt_required
#@admin_required
def update_book_details(bookId):
    """This method is for the admin to update details of a book or delete it"""
    try:
        bookId = int(bookId)
        # Retrieve a book with that ID from the DB.
        book_to_update = Library.query.filter_by(book_id=bookId).first()
        # Check if the book actually exists in the DB.
        if not book_to_update:
            return Response(json.dumps({'message': 'This book does not exist in the library.'}), status=200, \
             content_type = 'apllication/json')
        
        elif request.method == 'PUT':
            title = request.json.get('title')
            author = request.json.get('author')
            year = request.json.get('year')

            if title and title.strip() !="":
                book_to_update.title = title
            if author and author.strip() !="":
                book_to_update.author = author
            if year and year !="":
                book_to_update.year = year
         
            book_to_update.save_book_to_db()
            return Response(json.dumps({'message': 'Successfuly updated book details: {} by {} year {}'.format(title, author, year)}), status=200,\
             content_type='application/json')

        elif request.method == 'DELETE':
            book_to_update.delete_book()
            return Response(json.dumps({'message': 'You have deleted this book {}'.format(book_to_update.title)}), status=200,\
             content_type='application/json')
    except ValueError:
        return Response(json.dumps({'message': 'Invalid book ID'}), status=404, content_type='application/json')


@app.route('/api/v2/users/books/<book_id>', methods=['POST'])
@jwt_required
def borrow_book(book_id):
    """ This method allows a registered user to borrow a book"""
    try:
        bookID = int(book_id)
    except ValueError:
        return Response(json.dumps({'message': 'Enter a valid book ID'}))
    
    usermail = request.json.get('email')
    if usermail == None or usermail == "" or usermail.strip() =="":
            return Response(json.dumps({'message': 'Invalid. Please enter a vaild email'}))
    else:
        jti = get_raw_jwt()['jti']
        logged_in_user = get_jwt_identity()
        if logged_in_user != usermail or IssuedTokens.is_jti_blacklisted(jti):
            return Response(json.dumps({'message': 'Please login to receive a token'}))
        else:
            book_details = Library.get_book_by_id(bookID)
            if not book_details:
               return Response(json.dumps({'message': 'The library has no book with that ID'}))
            else:
                """processing the borrow request"""
                if request.method == "POST":
                    if book_details.is_not_borrowed == "False":
                        return Response(json.dumps({'message': 'This book has already been borrowed by another user'}))
                    borrower= UsersTable.get_user_by_email(usermail)
                    return_date = datetime.now() + timedelta(days=7)
                    book_now_borrowed = BookHistory(usermail=usermail,
                                                book_id=book_id,
                                                return_date=return_date)

                    return Response(json.dumps({**{"Message": "{} You have successfully borrowed a book".format(borrower)}, **book_now_borrowed.serialize}),\
                     status = 200, content_type='application/json')
                      
                    book_now_borrowed.save_book_to_db()
                    
                    # update book_is_not_borrowed in the library table in DB
                    book_details.is_not_borrowed = "False"
                    book_details.save_book_to_db()

                elif request.method == "PUT":
                    book_to_return = BookHistory.get_book_by_id(book_id)
                    if book_details.is_not_borrowed == "True":
                        return Response(json.dumps({'Message': 'This book has not been borrowed {}'.format(book_to_return)}), status = 200)
                    
                    # Now let's set the book status to available in book db.
                    book_details.is_not_borrowed = "False"
                    book_details.save_book_to_db()

                    # Set book status & return date in BookHistory db.
                    book_to_return.returned = True
                    book_to_return.return_date = datetime.now()
                    book_to_return.save_book_to_db()
                    return Response(json.dumps({**{"Message": "Book returned successfully"}, **book_details.serialize_history,
                         **book_to_return.serialize}), status = 204, content_type='application/json')

@app.route('/api/v2/users/books', methods=['GET'])
@jwt_required
def borrow_history():
    """This method showcases the borrowing history of a user"""
    # usermail = get_jwt_identity()
    # returned = request.args.get('returned')
    # if returned and returned == "false":
    #     books_not_returned = BookHistory.get_books_not_returned(usermail)
    #     if not books_not_returned:
    #         response = jsonify(
    #             {"Message": "You do not have a book that is not returned."})
    #     else:
    #         response = jsonify(
    #             History=[{**log.serialize, **log.book.serialize_history}
    #                      for log in books_not_returned]
    #         )
    # else:
    #     books_borrowed = BookHistory.get_user_history(usermail)
    #     if not books_borrowed:
    #         response = jsonify(
    #             {"Message": "You do not have a borrowing history."})
    #     else:
    #         response = jsonify(
    #             books=[{**borrow.serialize, **borrow.book.serialize_history}
    #                    for borrow in books_borrowed]
    #         )
    #  return response

@app.errorhandler(404)
def route_not_found(error=None):
        """This method handles a wrong endpoint."""
        return jsonify({
            'message': '{} is not a valid url. Please check your spelling'.format(request.url, request.method)
        }), 404

@app.errorhandler(405)
def method_not_found(error=None):
    """This method handles an unallowed endpoint."""
    return jsonify({
            'message': 'This method {} is not allowed on this endpoint'.format(request.method)}), 405


@app.errorhandler(500)
def internal_server_error(error=None):

    """This method handles an internal server error"""
    return jsonify({
            'message': 'Failed - Internal server error'}), 500