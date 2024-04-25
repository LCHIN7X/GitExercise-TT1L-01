# imports
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import database as db
from werkzeug.security import generate_password_hash
from email_validator import validate_email, EmailNotValidError
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

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

        try:
            email_info = validate_email(email,check_deliverability=False)
            normalized_email = email_info.normalized 

        except EmailNotValidError as e:
            flash("Invalid email address.",category="error")

        if len(username) < 2:
            flash("Username must be at least 2 characters long.",category="error")

        elif len(student_id) != 10:
            flash("Student ID must be 10 characters long.")
        
        elif len(password1) < 8:
            flash("Password must be at least 8 characters long.",category="error")
        
        elif password1 != password2:
            flash("Passwords do not match.",category="error")
        
        else:            
            user_in_db = User.query.filter(and_(User.email == normalized_email,
                                                User.student_id == student_id)).first()

            if user_in_db:
                flash("Account already exists",category="error")

            else: 
            # if user record is not in database, try to create new account
                try:
                    new_user_account = User(email=normalized_email,
                                            username=username,
                                            student_id=student_id,
                                            password=generate_password_hash(password1,method="scrypt"))
                    db.session.add(new_user_account)
                    db.session.commit()
                    flash("Account successfully created!",category="success")
                    return redirect(url_for("views.home"))
                
                except IntegrityError:
                    db.session.rollback()
                    flash("Username already taken, please enter a new username.",category="error")

    
    # if method is GET, render page
    return render_template("create_account.html")