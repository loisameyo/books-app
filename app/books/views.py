from flask import Flask
from flask import Response, request, json, jsonify, abort
from flask_jwt_extended import jwt_required

from app.models import BooksTable

from . import book

@book.route('/', methods = ['GET'])
@jwt_required
def retrieve_all_books():
    """Let's find out all the books in the library"""
    if request.method =="GET":
        all_books = BooksTable.query.all()
        if not all_books:
            return Response(json.dumps({'message': 'No books available in the BooksTable'}), \
            status=202, content_type='application/json')
        return jsonify({'books':[item.serialize for item in all_books], 'message': 'Books found'}), 200

@book.route('/<book_id>', methods = ['GET'])
@jwt_required
def retrieve_particular_book(book_id):
    """This method allows us to retrieve a particular book"""
    try:
        required_book_id = int(book_id)
        retrieved_book = BooksTable.query.filter_by(
            book_id=required_book_id).first()
        if not retrieved_book:
            return Response(json.dumps({'Message': 'There is no book with that ID in the BooksTable'}),\
             status=404, content_type='application/json')
        else:
            return jsonify({'book': retrieved_book.serialize, 'Message': 'Book successfully retrieved'}), 200
    except ValueError:
        return Response(json.dumps({'Message': 'Please enter a valid book ID'}), \
        status=404, content_type='application/json')
