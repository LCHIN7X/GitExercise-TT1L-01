### from flask import Blueprint, render_template
from flask import Blueprint, render_template, url_for,request,flash,redirect
import os
from flask_sqlalchemy import SQLAlchemy
from auth.models import db


# views = Blueprint("views",__name__)

### Define the Blueprint with optional custom paths for templates and static files
views = Blueprint(
    "views",
    __name__,
    template_folder="templates",
    static_folder="static",  # Ensure this folder exists in your project
    static_url_path="/static/views"  # Optional custom path for Blueprint static files
)

### @views.route("/home")
# @views.route("/")
# def home():
#     return render_template("base.html") 

@views.route("/add",methods=["GET","POST"])
def add():
    if request.method == "POST":
        username = request.form.get("username")
        faculty = request.form.get("faculty")
        faculty = faculty(name=faculty)
        db.session.add(faculty)
        db.session.commit()
        subject = request.form.get("subject")
        subject = subject(name=subject)
        db.session.add(subject)
        db.session.commit()
        Quantity = request.form.get("Quantity")
        Quantity = Quantity(name=Quantity)
        db.session.add(Quantity)
        db.session.commit()
        Price = request.form.get("Price")
        Price = Price(name=Price)
        db.session.add(Price)
        db.session.commit()
        photo = request.form.get("photo")
        Remark = request.form.get("Remark")
            
    return render_template("add-and-remove.html")

@views.route("/upload_form", methods=['GET', 'POST'])
def upload_form():
    return render_template("success.html")

@views.route("/secondhand-books", methods=['GET', 'POST'])
def secondhand():
    return render_template("secondhand-books.html")