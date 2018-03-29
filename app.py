from flask import Flask, request, Response, json
app=Flask (__name__)

books = {}

@app.route('/api/books', methods=['POST', 'GET'])
def save_book():
    if request.method == 'POST':
        book_name = request.form["name"]
        current_count = len(books)
        books[current_count + 1] = {'book_name': book_name, 'borrowed': False}
        return Response(json.dumps({'message': 'Successfully posted!'}), status=201, mimetype='application/json')

    if request.method == 'GET':
        retrieved_books = list(books.values())
        return Response(json.dumps({'books': retrieved_books}), status=200, mimetype='application/json')

@app.route('/api/books/<book_id>', methods=['GET', 'DELETE', 'PUT'])
def access_book(book_id):
    """This method accesses a book and performs an operation to it depending on the request method"""
    if request.method == 'GET':
        try:
            print("le books!",books, book_id)
            book = books[int(book_id)]
            print("retrieved book", books[int(book_id)])
            return Response(json.dumps({'book': book}), status=200, mimetype='application/json')
        except KeyError:
            return Response(json.dumps({'message': 'Invalid book Id'}), status=404, mimetype='application/json')

    if request.method == 'PUT':
        new_book_name = request.form['name']
        book_status = request.form['borrowed']
        try:
            book = books[int(book_id)]
            if book:
                books[int(book_id)] = {'book_name': new_book_name, 'borrowed': book_status}
                return Response(json.dumps({'message':'Updated Successfully'}), status=200, mimetype='application/json')
            else:
               return Response(json.dumps({'message': 'Invalid book Id'}), status=404, mimetype='application/json') 
        except KeyError:
            return Response(json.dumps({'message': 'Invalid book Id'}), status=404, mimetype='application/json')

    if request.method=='DELETE':
        try:
            book = books[int(book_id)]
            if book:
                del books[int(book_id)]
                return Response(json.dumps({'message':'Deleted Successfully'}), status=204, mimetype='application/json')
            else:
                return Response(json.dumps({'message': 'Invalid book Id'}), status=404, mimetype='application/json') 
        except KeyError:
            return Response(json.dumps({'message': 'Invalid book Id'}), status=404, mimetype='application/json')  

@app.route('/api/users/books/<book_id>', methods=['GET'])
def borrow_book(book_id):
    try:
        retrieved_book_info = books[int(book_id)]
        if retrieved_book_info['borrowed']:
            #Book has been borowed
            return Response(json.dumps({'message':'Book is borrowed'}), status=404, mimetype='application/json')
        else:
            #Book has not been borrowed
            retrieved_book_info['borrowed'] = True
            books[int(book_id)]= retrieved_book_info
            return Response(json.dumps({'message': 'Book issued'}), status=200, mimetype='application/json') 
    except KeyError:
        return Response(json.dumps({'message': 'Invalid book Id'}), status=404, mimetype='application/json')   


    
if __name__=='__main__':
    app.run()