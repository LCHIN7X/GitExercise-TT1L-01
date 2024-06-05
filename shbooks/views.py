from flask import Blueprint, render_template, redirect, url_for, request, flash
import os
from auth.models import User
from flask_login import current_user, login_required
from flask import session
from flask_uploads import UploadSet, IMAGES
from auth.models import db
from books.models import Book, Faculty, Subject
from .forms import Editbook
from werkzeug.utils import secure_filename
import sqlite3

####
shbooks = Blueprint(
    "shbooks",
    __name__,
    static_folder="static",
    template_folder="templates"  
)

photos = UploadSet('photos', IMAGES)

def get_db_connection():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    return con

@shbooks.route("/upload_form", methods=['GET', 'POST'])
def upload_form():
    return render_template("success.html")


@shbooks.route("/ownshop", methods=['GET', 'POST'])
def myshop():
    user_bg = current_user.profile_pic if current_user.is_authenticated else 'default_pfp.png'
    profile_pic = current_user.profile_pic if current_user.is_authenticated else 'default_pfp.png'
    bio = current_user.bio if current_user.is_authenticated else ''
    username = current_user.username if current_user.is_authenticated else ''
    faculties = Faculty.query.all()
    subjects = Subject.query.all()
    books = Book.query.all()
    form = Editbook(request.form)
    return render_template("ownshop.html", user_bg=user_bg, profile_pic=profile_pic, bio=bio, username=username, books=books, form=form, faculties=faculties, subjects=subjects,edit_book=None)  


@shbooks.route("/delete/<int:id>")
def delete(id):
    delete_book = Book.query.get_or_404(id)
    
    try:
        db.session.delete(delete_book)
        db.session.commit()
        flash('Book deleteted successfully', 'success')
        return redirect('../ownshop')
    except:
        flash('Book deleted failed', 'error')
        return redirect('../ownshop')

@shbooks.route('/test/<int:id>', methods=['POST', 'GET'] )
def testpage(id):
    edit_book = Book.query.get_or_404(id)
    faculties = Faculty.query.all() 
    subjects = Subject.query.all()  
    return render_template('editform.html', edit_book=edit_book, faculties=faculties, subjects=subjects)

@shbooks.route('/testfunction/<int:id>', methods=['POST', 'GET'])
def testfunction(id):
    edit_book = Book.query.get_or_404(id)
    if request.method == "POST":
        try:
            edit_book.price = float(request.form['price'])
            edit_book.stock = int(request.form['stock'])
            edit_book.faculty_id = request.form['faculty']
            faculty_name = request.form['faculty']

            faculty = Faculty.query.filter_by(name=faculty_name).first()
 
            edit_book.faculty_id = faculty.id
            
            db.session.commit()  

            flash('Book edited successfully', 'success')
            return redirect(url_for('shbooks.myshop'))
        except Exception as e:
            flash(f'Error editing book: {str(e)}', 'error')
            return redirect(url_for('shbooks.myshop'))

    return redirect(url_for('shbooks.myshop'))

@shbooks.route('/searchresult')
def searchresult():
    profile_pic = current_user.profile_pic if current_user.is_authenticated else 'default_pfp.png'
    bio = current_user.bio if current_user.is_authenticated else ''
    username = current_user.username if current_user.is_authenticated else ''
    searchword = request.args.get('x')
    books = Book.query.msearch(searchword,fields=['name','desc'],limit=3)
    facultiess = Faculty.query.join(Book,(Faculty.id == Book.faculty_id)).all()
    subjects = Subject.query.join(Book,(Subject.id == Book.subject_id)).all()
    return render_template('searchresult.html',profile_pic=profile_pic, bio=bio, username=username,books=books,facultiess=facultiess,subjects=subjects)