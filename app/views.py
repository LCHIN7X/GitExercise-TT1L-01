from flask import Blueprint, render_template 

views = Blueprint("views",__name__)

@views.route("/home")
def home():
    return render_template("base.html") 

@views.route("/add")
def add():
    return render_template("add-and-remove.html")