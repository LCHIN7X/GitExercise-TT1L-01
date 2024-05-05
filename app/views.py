### from flask import Blueprint, render_template
from flask import Blueprint, render_template, url_for,request,flash,redirect
import os
from flask_sqlalchemy import SQLAlchemy
from auth.models import User, db
from flask import session
from .models import Faculty, Subject, Quantity, Price, Books, db
from .forms import AddBookForm
from flask_uploads import UploadSet, IMAGES


# views = Blueprint("views",__name__)

### Define the Blueprint with optional custom paths for templates and static files
views = Blueprint(
    "views",
    __name__,
    template_folder="templates",
    static_folder="static",  # Ensure this folder exists in your project
    static_url_path="/static/views"  # Optional custom path for Blueprint static files
)

photos = UploadSet('photos', IMAGES)

### @views.route("/home")
# @views.route("/")
# def home():
#     return render_template("base.html") 

@views.route("/add", methods=["GET", "POST"])
def add():
    form = AddBookForm()

    if request.method == "POST" and form.validate_on_submit():
        current_username = session.get('username')
        username = form.username.data
        if current_username != username:
            return render_template("add-and-remove.html", username=current_username, error="Username does not match logged in user")

        faculty_name = form.faculty.data
        subject_name = form.subject.data
        quantity_value = form.quantity.data
        price_value = form.price.data
        remark = form.remark.data

        faculty = Faculty.query.filter_by(name=faculty_name).first()
        if not faculty:
            faculty = Faculty(name=faculty_name)
            db.session.add(faculty)
            db.session.commit()

        subject = Subject.query.filter_by(name=subject_name).first()
        if not subject:
            subject = Subject(name=subject_name)
            db.session.add(subject)
            db.session.commit()

        quantity = Quantity(value=quantity_value)
        db.session.add(quantity)
        db.session.commit()

        price = Price(value=price_value)
        db.session.add(price)
        db.session.commit()

        photo_filename = photos.save(form.photo.data)

        book = Books(
            username=username,
            faculty_id=faculty.id,
            subject_id=subject.id,
            quantity_id=quantity.id,
            price_id=price.id,
            photo=photo_filename,
            remark=remark
        )
        db.session.add(book)
        db.session.commit()

        return redirect(url_for('views.upload_form'))

    return render_template("add-and-remove.html", form=form)

@views.route("/upload_form", methods=['GET', 'POST'])
def upload_form():
    return render_template("success.html")

@views.route("/secondhand-books", methods=['GET', 'POST'])
def secondhand():
    return render_template("secondhand-books.html")