from flask import Blueprint, render_template

auth = Blueprint("auth",__name__)

@auth.route("/create_account")
def create_account():
    return render_template("create_account.html")