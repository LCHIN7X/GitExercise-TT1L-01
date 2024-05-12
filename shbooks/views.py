### from flask import Blueprint, render_template
from flask import Blueprint, render_template, redirect, url_for, request, flash
import os
from auth.models import User
from flask import session
from flask_uploads import UploadSet, IMAGES
from auth.models import db
from books.models import Book, Faculty, Subject
from .forms import Editbook
from werkzeug.utils import secure_filename

####
# from main import User, SecondHandBooks,db

# db = SQLAlchemy()

# views = Blueprint("views",__name__)

### Define the Blueprint with optional custom paths for templates and static files
shbooks = Blueprint(
    "shbooks",
    __name__,
    static_folder="static",
    template_folder="templates"  # Ensure this folder exists in your project
)

photos = UploadSet('photos', IMAGES)

### @views.route("/home")
# @views.route("/")
# def home():
#     return render_template("base.html")


@shbooks.route("/upload_form", methods=['GET', 'POST'])
def upload_form():
    return render_template("success.html")

@shbooks.route("/ownshop", methods=['GET', 'POST'])
def myshop():
    faculties = Faculty.query.all()
    subjects = Subject.query.all()
    form = Editbook(request.form)

    if request.method == 'POST':
        print("Form submitted")
        if form.validate():
            print("Form validated")  
            name = form.name.data
            price = form.price.data
            stock = form.stock.data
            selected_faculty = request.form.get('faculty')
            selected_subject = request.form.get('subject')
            image = form.image.data
            print(f"Name: {name}, Price: {price}, Stock: {stock}, Faculty: {selected_faculty}, Subject: {selected_subject}, Image: {image}")
            
            # Handle file upload
            if 'image' in request.files:
                image = photos.save(request.files['image'])
                print("Image uploaded")
            else:
                image = None
            print(f"Image: {image}")
            
            book_id = request.form.get('book_id')
            if book_id:
                book = Book.query.get(book_id)
                if book:
                    book.name = name
                    book.price = price
                    book.stock = stock
                    book.faculty = selected_faculty
                    book.subject = selected_subject
                    if image:
                        book.image = image  
                    db.session.commit()
                    flash('Book updated successfully', 'success')
                    return redirect(url_for('shbooks.myshop'))
                else:
                    flash('Book not found', 'error')
            else:
                book = Book(
                    name=name,
                    price=price,
                    stock=stock,
                    faculty=selected_faculty,
                    subject=selected_subject,
                    image=image, 
                )
                db.session.add(book)
                db.session.commit()
                flash('Book added successfully', 'success')
                return redirect(url_for('shbooks.myshop'))
        else:
            flash('Form validation failed', 'error')

    books = Book.query.all()
    return render_template("ownshop.html", form=form, books=books, faculties=faculties, subjects=subjects)