from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import database as db

auth = Blueprint("auth",__name__)

@auth.route("/create_account",methods=["GET","POST"])
def create_account():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        student_id = request.form.get("student_id")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

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
            user_in_db = User.query.filter_by(email=email).first()

            if not user_in_db:
                new_user_account = User(email=email,
                                    username=username,
                                    student_id=student_id,
                                    password=password1)
                db.session.add(new_user_account)
                db.session.commit()
                return redirect(url_for("views.home"))

            else:
                flash("Account already exists.",category="error")
    
    return render_template("create_account.html")