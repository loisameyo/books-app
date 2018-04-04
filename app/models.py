import uuid
class Users():
    def __init__(self, email, password):
        self.email = email
        self.password = password
     
    @property
    def serialize(self):
        return{
    "user_mail":self.email,
    "user_pass":self.password
    
     } 

class Books():
    def __init__(self, name, author, pub_year, id=None):
        self.id = uuid.uuid4().hex if id is None else id
        self.name = name
        self.author = author
        self.year = pub_year
        self.status = True
        self.count = 0

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "author": self.author,
            "publication year": self.year,
            "Book status": self.status,
            "Book count": self.count,
        }
      


