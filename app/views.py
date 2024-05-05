### from flask import Blueprint, render_template
from flask import Blueprint, render_template, url_for,request,redirect
import os
from flask_sqlalchemy import SQLAlchemy
from auth.models import User, db
from flask import session
from .models import Faculty, Subject, Quantity, Price, Books, db
from .forms import AddBookForm,RemoveBookForm
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
    add_form = AddBookForm()
    remove_form = RemoveBookForm()
    if request.method == "POST":
        if 'submit_add' in request.form and add_form.validate_on_submit():
            username = add_form.username.data
            faculty_name = add_form.faculty.data
            subject_name = add_form.subject.data
            quantity_value = add_form.quantity.data
            price_value = add_form.price.data
            remark = add_form.remark.data

            faculty = Faculty.query.filter_by(name=faculty_name).first()
            if not faculty:
                faculty = Faculty(name=faculty_name)
                db.session.add(faculty)

            subject = Subject.query.filter_by(name=subject_name).first()
            if not subject:
                subject = Subject(name=subject_name)
                db.session.add(subject)

            quantity = Quantity(value=quantity_value)
            db.session.add(quantity)

            price = Price(value=price_value)
            db.session.add(price)

            photo_filename = 'photos/' + add_form.photo.data.filename
            add_form.photo.data.save(photo_filename)

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

            return redirect(url_for('upload_form'))

        elif 'submit_remove' in request.form and remove_form.validate_on_submit():
            book_id_to_remove = remove_form.books.data
            book_to_remove = Books.query.get(book_id_to_remove)
            if book_to_remove:
                db.session.delete(book_to_remove)
                db.session.commit()

            return redirect(url_for('upload_form'))

    remove_form.books.choices = [(book.id, book.subject.name) for book in Books.query.all()]

    return render_template("add-and-remove.html", add_form=add_form, remove_form=remove_form)

@views.route("/upload_form", methods=['GET', 'POST'])
def upload_form():
    return render_template("success.html")

@views.route("/secondhand-books", methods=['GET', 'POST'])
def secondhand():
    return render_template("secondhand-books.html")