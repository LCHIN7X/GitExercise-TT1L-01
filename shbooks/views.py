### from flask import Blueprint, render_template
from flask import Blueprint, render_template, url_for,request,flash,redirect
import os
from flask_sqlalchemy import SQLAlchemy
from auth.models import User
from flask import session
from .models import SecondHandBooks,shbooks_Faculty,shbooks_Subject
from .forms import AddBookForm,RemoveBookForm
from flask_uploads import UploadSet, IMAGES
from auth.models import db

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

@shbooks.route('/addFnS', methods=['GET','POST'])
def addFnS():
    if request.method == "POST":
        getfaculty = request.form.get('faculty')
        faculty = shbooks_Faculty(name=getfaculty)
        db.session.add(faculty)
        flash(f'Faculty {getfaculty} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('shbooks.addFnS'))
    
    return render_template('addFnS.html', shbfaculties='shbfaculties')




@shbooks.route('/addsub', methods=['GET','POST'])
def addsub():
    if request.method =="POST":
        getfaculty = request.form.get('subject')
        sub = shbooks_Subject(name=getfaculty)
        db.session.add(sub)
        flash(f'Subject {getfaculty} was added to your datebase','success')
        db.session.commit()
        return redirect(url_for('shbooks.addFnS'))
    
    return render_template('addfaculty.html') 

@shbooks.route("/add", methods=["GET", "POST"])
def add():
    return render_template("add-and-remove.html")

@shbooks.route("/upload_form", methods=['GET', 'POST'])
def upload_form():
    return render_template("success.html")

@shbooks.route("/secondhand-books", methods=['GET', 'POST'])
def secondhand():
    return render_template("secondhand-books.html")

@shbooks.route("/ownshop", methods=['GET', 'POST'])
def myshop():
    return render_template("ownshop.html")