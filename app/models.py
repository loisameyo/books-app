import uuid
class User():
    def __init__(self,id, email, password):
        self.id = id
        self.email = email
        self.password = password

class Books():
    def __init__(self, name, author, pub_year, id=None):
        self.id = id #uuid.uuid4().hex if id is None else id
        self.name = name
        self.author = author
        self.year = pub_year

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "author": self.author,
            "publication year": self.year
        }

    



