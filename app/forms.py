from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, InputRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired

class PropertyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    rooms = StringField('Number of Bedrooms', validators=[InputRequired()])
    bathrooms = StringField('Number of Bathrooms', validators=[InputRequired()])
    location = StringField('Location', validators=[DataRequired()])
    price = StringField('Price', validators=[InputRequired()])
    type = SelectField('Type', choices=[('House', 'House'), ('Apartment', 'Apartment')], validators=[InputRequired()])
    description = TextAreaField('Description')
    photoname = FileField('Photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])