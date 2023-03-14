"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

from app import app,db
import os
from flask import render_template, request, redirect, url_for,flash
from werkzeug.utils import secure_filename
from .forms import PropertyForm
from app.models import Property
from flask.helpers import send_from_directory



###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Ashli-ann")

@app.route('/newproperty/', methods=['GET', 'POST'])
def add_property():
    form = PropertyForm()
    if form.validate_on_submit():
        # Save the file to disk
         # Extract form data
        title = form.title.data
        description = form.description.data
        rooms = form.rooms.data
        bathrooms = form.bathrooms.data
        price = form.price.data
        propertyType = form.type.data
        location = form.location.data
        photo = form.photoname.data
        photo_name = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_name)) 
        '''Add new property to db and commit'''
        property = Property(title, description, rooms, bathrooms, price, propertyType, location, photo_name)
        db.session.add(property)
        db.session.commit()
        flash('Property added successfully.','success')
        return redirect(url_for('properties'))
    return render_template('newproperty.html', form=form)

@app.route('/properties/')
def properties():
    properties = Property.query.all()
    return render_template('properties.html', properties=properties)

@app.route('/properties/<int:pid>')
def property_details(pid):
    property = Property.query.get(int(pid))
    return render_template('property_details.html', property=property)

@app.route('/properties/<photoname>')
def getImage(photoname):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), photoname)
###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
