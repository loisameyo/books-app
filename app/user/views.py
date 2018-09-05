from flask import Flask
from flask import Response, request, json, jsonify, abort
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_raw_jwt


from . import user
from app.models import UsersTable, BooksTable, BookHistory, RevokedTokens
from app.decorators import admin_required



@user.route('/books/<book_id>', methods=['POST', 'PUT'])
@jwt_required
def borrow_book(book_id):
    """ This method allows a registered user to borrow a book"""
    try:
        book_id = int(book_id)
    except ValueError:
        return Response(json.dumps({'message': 'Enter a valid book ID'}), status=404, content_type='application/json')
    
    usermail = request.json.get('email')
    if usermail is None or usermail == "" or usermail.strip() =="":
            return Response(json.dumps({'message': 'Invalid. Please enter a vaild email'}), status=400, content_type='application/json')
    else:
        jti = get_raw_jwt()['jti']
        logged_in_user = get_jwt_identity()
        if logged_in_user != usermail or RevokedTokens.is_jti_blacklisted(jti):
            return Response(json.dumps({'message': 'Unknown user. Please register and login to receive a token'}),\
             status=401, content_type='application/json')
        else:
            one_book = BooksTable.query.filter_by(book_id=book_id).first()
            # book_details = BooksTable.retrieve_book_by_id(book_id)
            if not one_book:
                return Response(json.dumps({'message': 'The library has no book with that ID'}), 
                status=404, content_type='application/json')
            else:
                """processing the borrow request"""
                if request.method == "POST":
                    has_borrowed = BookHistory.query.filter_by(bh_book_id=book_id, bh_usermail=get_jwt_identity())
                    if one_book.is_not_borrowed is False:
                        if has_borrowed:
                            return Response(json.dumps({'message': "You have already borrowed this book"}),
                             status=403, content_type='apllication/json')
                        return Response(json.dumps({'message': 
                            'This book has already been borrowed by another user'}), status = 404, 
                             content_type='application/json')
                    return_date = datetime.now() + timedelta(days=7)
                    book_now_borrowed = BookHistory(bh_usermail=usermail,
                                                bh_book_id=book_id,
                                                return_date=return_date)
                    book_now_borrowed.save_book_to_db()
                    
                    # update book_is_not_borrowed in the library table in DB
                    one_book.is_not_borrowed = False
                    one_book.save_book_to_db()
                    return Response(json.dumps({"Message": "You have successfully borrowed a book",
                     **book_now_borrowed.serialize}), status = 200, content_type='application/json')

                elif request.method == "PUT":
                    book_to_return = BookHistory.retrieve_book_by_id_and_usermail(book_id, usermail)
                    if one_book.is_not_borrowed is True:
                        return Response(json.dumps({'Message': 'This book has not been borrowed {}'
                        .format(one_book.book_title)}), status = 404, content_type='application/json')
                    
                    # Now let's set the book status to available in book db.
                    one_book.is_not_borrowed = True
                    one_book.save_book_to_db()

                    # Set book status & return date in BookHistory db.
                    book_to_return.book_returned = True
                    book_to_return.return_date = datetime.now()
                    book_to_return.save_book_to_db()
                    return Response(json.dumps({"Message": "Book returned successfully",
                     **one_book.serialize_history, **book_to_return.serialize}), 
                     status = 200, content_type='application/json')
                                

@user.route('/books', methods=['GET'])
@jwt_required
def borrow_history():
    user_history = BookHistory.query.paginate()
    current_page = user_history.page
    all_pages = user_history.pages
    next_page = user_history.next_num
    prev_page = user_history.prev_num

    """This method showcases the borrowing history of a user and a user's unreturned books"""
    usermail = get_jwt_identity()
    returned = request.args.get('returned')
    BookHistory.query.filter_by(bh_usermail=usermail).first()

    if returned and returned == "false":
        books_not_returned = BookHistory.get_unreturned_books(usermail)
        if not books_not_returned:
            return Response(json.dumps({"Message": "You do not have a book that is not returned."}), status = 404,\
             content_type='application/json')
        else:
            results = [item.serialize for item in books_not_returned]
            return jsonify({"book_history": results, "current_page": current_page, "all_pages": all_pages, 
        "next_page": next_page, "previous_page": prev_page}), 200
            
    else:
        books_borrowed = BookHistory.get_user_history(usermail)
        if not books_borrowed:
            return Response(json.dumps({"Message": "You do not have a book that is not returned."}), status = 404,\
             content_type='application/json')
        else:
            results = [item.serialize for item in books_borrowed]
            return jsonify({"book_history": results, "current_page": current_page, "all_pages": all_pages, 
            "next_page": next_page, "previous_page": prev_page}), 200
