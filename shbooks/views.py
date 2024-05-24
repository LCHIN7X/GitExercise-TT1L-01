from flask import Blueprint, render_template, redirect, url_for, request, flash
import os
from auth.models import User
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
    
@shbooks.route("/ownshop", methods=['GET', 'POST'])
def myshop():
    faculties = Faculty.query.all()
    subjects = Subject.query.all()
    books = Book.query.all()
    form = Editbook(request.form)
    return render_template("ownshop.html", books=books, form=form, faculties=faculties, subjects=subjects,edit_book=None)  


@shbooks.route("/delete/<int:id>")
def delete(id):
    delete_book = Book.query.get_or_404(id)
    
    try:
        db.session.delete(delete_book)
        db.session.commit()
        flash('Book deleteted successfully', 'success')
        return redirect('/ownshop')
    except:
        flash('Book deleted failed', 'error')
        return redirect('/ownshop')

@shbooks.route('/test/<int:id>', methods=['POST', 'GET'] )
def testpage(id):
    edit_book = Book.query.get_or_404(id)
    return render_template('editform.html', edit_book=edit_book)

@shbooks.route('/testfunction/<int:id>', methods=['POST', 'GET'])
def testfunction(id):
    edit_book = Book.query.get_or_404(id)
    if request.method == "POST":
        try:
            image = request.files['image']
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                image.save(os.path.join('shbooks/static/images', filename))
                edit_book.image = filename
            
            edit_book.name = request.form['name']
            edit_book.price = float(request.form['price'])
            edit_book.stock = int(request.form['stock'])
            edit_book.faculty_id = request.form['faculty']
            edit_book.subject_id = request.form['subject'] 

            faculty_name = request.form['faculty']
            subject_name = request.form['subject']
            
           
            faculty = Faculty.query.filter_by(name=faculty_name).first()
            subject = Subject.query.filter_by(name=subject_name).first()

            if not faculty or not subject:
                flash('Invalid faculty or subject name', 'error')
                return redirect(url_for('shbooks.myshop'))

            edit_book.faculty_id = faculty.id
            edit_book.subject_id = subject.id
            
            db.session.commit()  

            flash('Book edited successfully', 'success')
            return redirect(url_for('shbooks.myshop'))
        except Exception as e:
            flash(f'Error editing book: {str(e)}', 'error')
            return redirect(url_for('shbooks.myshop'))

    return redirect(url_for('shbooks.myshop'))

@shbooks.route('/searchresult')
def searchresult():
    searchword = request.args.get('x')
    books = Book.query.msearch(searchword,fields=['name','desc'],limit=3)
    return render_template('searchresult.html',books=books)
