from flask import Blueprint, render_template, redirect, url_for, request, flash
import os
from auth.models import User
from flask_login import current_user, login_required
from auth.models import db
from books.models import Book, Faculty, Subject
from books.invoice import Rating
from .forms import Editbook

import sqlite3

shbooks = Blueprint(
    "shbooks",
    __name__,
    static_folder="static",
    template_folder="templates"
)

def get_db_connection():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    return con

@shbooks.route("/ownshop", methods=['GET', 'POST'])
@login_required
def myshop():
    user_bg = current_user.profile_pic if current_user.is_authenticated else 'default_pfp.png'
    profile_pic = current_user.profile_pic if current_user.is_authenticated else 'default_pfp.png'
    bio = current_user.bio if current_user.is_authenticated else ''
    username = current_user.username if current_user.is_authenticated else ''
    faculties = Faculty.query.all()
    subjects = Subject.query.all()
    books = Book.query.filter_by(user_id=current_user.id).all()  # Filter books by current user
    form = Editbook(request.form)
    return render_template("ownshop.html", user_bg=user_bg, profile_pic=profile_pic, bio=bio, username=username, books=books, form=form, faculties=faculties, subjects=subjects, edit_book=None)

@shbooks.route("/delete/<int:id>", methods=['POST'])
@login_required
def delete(id):
    delete_book = Book.query.get_or_404(id)
    if delete_book.user_id != current_user.id:
        flash('Unauthorized action', 'error')
        return redirect(url_for('shbooks.myshop'))

    
    try:
        db.session.query(Rating).filter_by(book_id=id).delete()
        db.session.commit()
    except Exception as e:
        flash(f'Failed to delete associated ratings: {str(e)}', 'error')

    try:
        db.session.delete(delete_book)
        db.session.commit()
        flash('Book deleted successfully', 'success')
    except Exception as e:
        flash(f'Failed to delete the book: {str(e)}', 'error')

    return redirect(url_for('shbooks.myshop'))




@shbooks.route('/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def edit(id):
    edit_book = Book.query.get_or_404(id)
    if edit_book.user_id != current_user.id:
        flash('Unauthorized action', 'error')
        return redirect(url_for('shbooks.myshop'))
        
    faculties = Faculty.query.all()
    subjects = Subject.query.all()
    if request.method == 'POST':
        try:
            edit_book.price = float(request.form['price'])
            edit_book.stock = int(request.form['stock'])
            faculty_name = request.form['faculty']

            faculty = Faculty.query.filter_by(name=faculty_name).first()
            if faculty:
                edit_book.faculty_id = faculty.id
            else:
                flash('Selected faculty not found', 'error')
                return redirect(url_for('shbooks.edit', id=id))

            db.session.commit()
            flash('Book edited successfully', 'success')
            return redirect(url_for('shbooks.myshop'))
        except Exception as e:
            flash(f'Error editing book: {str(e)}', 'error')
            return redirect(url_for('shbooks.edit', id=id))

    return render_template('editform.html', edit_book=edit_book, faculties=faculties, subjects=subjects)

@shbooks.route('/searchresult')
@login_required
def searchresult():
    user = current_user
    profile_pic = current_user.profile_pic if current_user.is_authenticated else 'default_pfp.png'
    bio = current_user.bio if current_user.is_authenticated else ''
    username = current_user.username if current_user.is_authenticated else ''
    searchword = request.args.get('x')
    

    books = Book.query.msearch(searchword, fields=['name', 'desc']).filter(Book.user_id == current_user.id).limit(3).all()
    
    return render_template('searchresult.html', profile_pic=profile_pic, bio=bio, username=username, books=books,user=user)





