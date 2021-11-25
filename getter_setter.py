import inspect
from db_poo import get_context

class User:
    def __init__(self, **params):
        self.id = params.get('id', 1)
        self.nom = params.get('nom')
        self.prenom = params.get('prenom')

    @property # si pas de paramètre donc pas besoin de parenthèses
    def NOMPrenom(self):
        return f'{self.nom.upper()} {self.prenom}'

    @classmethod
    @get_context
    def get(cls):
        print('get')
        print(x)

    def id_increment(self, val):
        return self.id + val

    def __setitem__(self, key, value):
          setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

def index():
    x=100
    print('index')
    User.get()
index()

objet = User(nom='Drouillet', prenom='Baptiste')
print(objet['id'])
print(objet['NOMPrenom'])

objet['age'] = 16
print(objet['age'])

from uuid import uuid4

uuid = uuid4()

print(type(uuid))
print(uuid == str(uuid))
