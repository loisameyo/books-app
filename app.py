from flask import Flask, request, Response, json
app=Flask (__name__)

books = {}

@app.route('/api/books', methods=['POST'])
def save_book():
    if request.method == 'POST':
        book_name = request.form["name"]
        current_count = len(books)
        books[current_count + 1] = book_name
        return Response(json.dumps({'message': 'Successfully posted!'}), status=201, mimetype='application/json')

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
        try:
            book = books[int(book_id)]
            if book:
                books[int(book_id)] = new_book_name
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

    
if __name__=='__main__':
    app.run()