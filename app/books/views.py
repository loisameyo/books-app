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
        all_books = BooksTable.query.paginate()
        books = all_books.items
        current_page = all_books.page
        all_pages = all_books.pages
        next_page = all_books.next_num
        prev_page = all_books.prev_num
        if not all_books:
            return Response(json.dumps({'message': 'No books available in the BooksTable'}), \
            status=404, content_type='application/json')
        books_retrieved = [item.serialize for item in books]
        return jsonify({'books': books_retrieved, "current_page": current_page, "all_pages": all_pages, 
        "next_page": next_page, "previous_page": prev_page}), 200

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
