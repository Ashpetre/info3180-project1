from . import db
import unicodedata

# Requires client-side validation

class Property(db.Model):
    __tablename__ = 'property'
    pid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column("title",db.String(80))
    description = db.Column("description",db.String(800))
    rooms = db.Column("rooms",db.String(3))
    bathroom = db.Column("bathroom",db.String(3)) 
    price = db.Column("price",db.String(12)) 
    type = db.Column("prop_type",db.String(9))
    location = db.Column("prop_loc",db.String(80))
    photoname = db.Column("photoname",db.String(80))

    def __init__(self, title, description, rooms, bathroom, price, type, location, photoname):
        self.title = title
        self.description = description
        self.rooms = rooms
        self.bathroom = bathroom
        self.price = price
        self.type = type
        self.location = location
        self.photoname = photoname

    def get_id(self):
        try:
            return unicodedata(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Property %r>' % (self.title)
