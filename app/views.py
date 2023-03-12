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

app.config['UPLOAD_FOLDER'] = '/path/to/uploads'

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
        filename = secure_filename(form.photo.data.filename)
        form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Save the property to the database
        property = Property(title=form.title.data, bedrooms=form.bedrooms.data, bathrooms=form.bathrooms.data, location=form.location.data, price=form.price.data, type=form.type.data, description=form.description.data, photo_name=filename)
        db.session.add(property)
        db.session.commit()
        flash('Property added successfully.','success')
        return redirect(url_for('index'))
    return render_template('newproperty.html', form=form)

@app.route('/properties/')
def properties():
    properties = Property.query.all()
    return render_template('properties.html', properties=properties)

@app.route('/properties/<int:property_id>')
def property_details(property_id):
    property = Property.query.get(property_id)
    return render_template('property_details.html', property=property)

@app.route('/properties/<filename>')
def getImage(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']),filename)
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
