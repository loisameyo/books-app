from flask import Flask, Response, request, json, jsonify, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_raw_jwt

from . import admin
from app.decorators import admin_required
from app.models import BooksTable, UsersTable

@admin.route('/books', methods=['POST'])
@jwt_required
@admin_required
def post_book():
    """This method allows a user to add a new book"""
    if request.method == "POST":
        title = request.json.get('title')
        author = request.json.get('author')
        year = request.json.get('pub_year')

        if title is None or title.strip()=="":
            return Response(json.dumps({'message': 'Give a valid book title.'}), content_type = 'apllication/json')
        if author is None or author.strip()=="":
            return Response(json.dumps({'message': 'Give a valid book author.'}), content_type = 'apllication/json')
        if year is None or year.strip()=="":
            return Response(json.dumps({'message': 'Give a valid year'}), content_type = 'apllication/json')

        
        new_book = BooksTable(
            book_title=title, book_author=author, publication_year=year)
        try:
            new_book.save_book_to_db()
        except Exception:
            return Response(json.dumps({'message': 'Book already exists'}))
        return Response(json.dumps({'message': \
        'You have successfully added the book  {}  by author  {}  published in the year {}'\
        .format(title, author, year)}), status=201, content_type='application/json')

@admin.route('/books/<bookId>', methods=['PUT', 'DELETE'])
@jwt_required
@admin_required
def update_book_details(bookId):
    """This method is for the admin to update details of a book or delete it"""
    try:
        bookId = int(bookId)
        # Retrieve a book with that ID from the DB.
        book_to_update = BooksTable.query.filter_by(book_id=bookId).first()
        # Check if the book actually exists in the DB.
        if not book_to_update:
            return Response(json.dumps({'message': 'This book does not exist in the library.'}),\
             status=404, content_type = 'apllication/json')
        
        elif request.method == 'PUT':
            title = request.json.get('title')
            author = request.json.get('author')
            year = request.json.get('year')

            if title and title.strip() !="":
                book_to_update.title = title
            if author and author.strip() !="":
                book_to_update.author = author
            if year:
                book_to_update.year = year
         
            book_to_update.save_book_to_db()
            return Response(json.dumps({'message': 'Successfully updated book details'}),
             status=200, content_type='application/json')

        elif request.method == 'DELETE':
            book_to_update.delete_book()
            return Response(json.dumps({'message': 'You have deleted this book {}'\
            .format(book_to_update.book_title)}),
             status=200,content_type='application/json')
    except ValueError:
        return Response(json.dumps({'message': 'Invalid book ID'}), status=404, 
        content_type='application/json')


