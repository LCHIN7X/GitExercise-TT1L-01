# imports
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import database as db

# ------------------------------- CODE ---------------------------------------------

# create new flask Blueprint with the name 'auth'
auth = Blueprint("auth",__name__)

# define route for creating account (/create_account)
# set HTTP methods to GET and POST
@auth.route("/create_account",methods=["GET","POST"])
def create_account():
    #  if method is POST, retrieve input field values to be validated
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        student_id = request.form.get("student_id")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        #  check if credentials meet the program requirements
        if len(email) < 5:
            flash("Please enter a valid email address.",category="error")

        elif len(username) < 2:
            flash("Username must be at least 2 characters long.",category="error")

        elif len(student_id) != 10:
            flash("Student ID must be 10 characters long.")
        
        elif len(password1) < 8:
            flash("Password must be at least 8 characters long.",category="error")
        
        elif password1 != password2:
            flash("Passwords do not match.",category="error")
        
        else:
            # if credentials meet the requirements, first check if user already has an account.
            user_in_db = User.query.filter_by(email=email).first()

            # if user record is not in database, create new account
            if not user_in_db:
                new_user_account = User(email=email,
                                    username=username,
                                    student_id=student_id,
                                    password=password1)
                db.session.add(new_user_account)
                db.session.commit()
                return redirect(url_for("views.home"))

            # if user does have an account, show error message
            else:
                flash("Account already exists.",category="error")
    
    # if method is GET, render page
    return render_template("create_account.html")