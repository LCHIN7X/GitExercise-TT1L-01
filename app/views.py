from flask import Blueprint, render_template 

views = Blueprint("views",__name__)

@views.route("/home")
def home():
    return render_template("base.html")

@views.route("/create_account")
def create_account():
    return render_template("create_account.html")