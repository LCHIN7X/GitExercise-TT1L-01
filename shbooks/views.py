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


@shbooks.route("/upload_form", methods=['GET', 'POST'])
def upload_form():
    return render_template("success.html")

@shbooks.route("/ownshop", methods=['GET', 'POST'])
def myshop():
    return render_template("ownshop.html")