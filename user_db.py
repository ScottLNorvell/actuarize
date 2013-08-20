
from google.appengine.ext import db

class User(db.Model):
    id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    name = db.StringProperty(required=True)
    access_token = db.StringProperty(required=True)
    gender = db.StringProperty()
    friend_data = db.TextProperty()
    
#class MovieDB(db.Model):
#    movie_id = db.StringProperty(required=True)
#    movie_data = db.TextProperty(required=True)
#    created = db.DateTimeProperty(auto_now_add=True)
    