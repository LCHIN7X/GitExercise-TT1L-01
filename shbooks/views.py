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
    books = Book.query.all()
    return render_template("ownshop.html", books=books, form=form, faculties=faculties, subjects=subjects)


# @shbooks.route("/edit/<int:id>", methods=['GET', 'POST'])
# def edit(id):
#     edit_book = Book.query.get_or_404(id)
#     if request.method == "POST":
#         edit_book.image = request.form['image']
#         edit_book.name = request.form['name']
#         edit_book.price = request.form['price']
#         edit_book.stock = request.form['stock']
#         edit_book.faculty = request.form['faculty']
#         edit_book.subject = request.form['subject']
        
#         try:
#             db.session.commit()
#             flash('Book edited successfully', 'success')
#             return redirect(url_for('shbooks.myshop'))
#         except:
#             flash('Failed to edit book', 'error')
#             return redirect(url_for('shbooks.myshop'))
    
#     # Ensure edit_book has the id attribute
#     print("Edit Book ID:", edit_book.id)
    
#     return render_template("ownshop.html", edit_book=edit_book)

            
    


@shbooks.route("/delete/<int:id>")
def delete(id):
    delete_book = Book.query.get_or_404(id)
    
    try:
        db.session.delete(delete_book)
        db.session.commit()
        flash('Book deleteted successfully', 'success')
        return redirect(url_for('shbooks.myshop'))
    except:
        flash('Book deleted failed', 'error')
        return redirect(url_for('shbooks.myshop'))
