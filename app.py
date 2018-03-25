from flask import Flask, request
app=Flask (__name__)

@app.route('/api/books', methods=['GET','POST','DELETE','PUT'])
def save():
    if request.method == 'GET':
        return "Looks good!"
    
if __name__=='__main__':
    app.run()