from . import db


# Requires client-side validation

class Property(db.Model):
    __tablename__ = 'property'
    pid = db.Column(db.Integer, primary_key=True)
    title = db.Column("title",db.String(80))
    description = db.Column("description",db.String(800))
    rooms = db.Column("rooms",db.String(3))
    bathroom = db.Column("bathroom",db.String(3)) 
    price = db.Column("price",db.String(12)) 
    property_type = db.Column("property_type",db.String(9))
    location = db.Column("location",db.String(80))
    photo_name = db.Column("photoname",db.String(80))

    def __init__(self, title, description, rooms, bathrooms, price, propertyType, location, photo_name):
        self.title = title
        self.description = description
        self.rooms = rooms
        self.bathrooms = bathrooms
        self.price = price
        self.property_type = propertyType
        self.location = location
        self.photo_name = photo_name

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Property %r>' % (self.title)
