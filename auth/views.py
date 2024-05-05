# imports
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, login_required, logout_user, current_user

# ------------------------------- CODE ---------------------------------------------

# create new flask Blueprint with the name 'auth'
auth = Blueprint("auth",__name__,template_folder="templates",static_folder="static")

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

        # set default value for normalized email 
        normalized_email = None

        #  check if credentials meet the program requirements
        #  validate email
        try:
            email_info = validate_email(email,check_deliverability=True)
            normalized_email = email_info.normalized 

            if len(username) < 2:
                flash("Username must be at least 2 characters long.",category="error")

            elif len(student_id) != 10:
                flash("Student ID must be 10 characters long.",category="error")
        
            elif len(password1) < 8:
                flash("Password must be at least 8 characters long.",category="error")
            
            elif password1 != password2:
                flash("Passwords do not match.",category="error")
        
            else:            
                user_in_db = User.query.filter(or_(User.email == normalized_email, User.student_id == student_id)).first()

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
                        return redirect(url_for("auth.login"))

                # if UNIQUE constraint fails:     
                    except IntegrityError:
                        db.session.rollback()
                        flash("Username already taken, please enter a new username.",category="error")

        except EmailNotValidError as e:
            flash("Invalid email address.",category="error")


    # if method is GET, render page
    return render_template("create_account.html",current_page="create_account",current_user=current_user)


#  define route for login (/login)
@auth.route("/login",methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        student_id = request.form.get('student_id')
        password = request.form.get('password') 

        #  check if credentials entered exist in User table
        user_in_db = User.query.filter_by(email=email, 
                                          student_id=student_id).first()
        
        if user_in_db:
            # if user account exists, first check if password is correct
            if check_password_hash(user_in_db.password, password):
                flash(f"Hello {user_in_db.username}, You Are Now Logged In!",category='success')
                login_user(user_in_db, remember=True)

                if email == "admin@gmail.com" and student_id == "super_user":
                    return redirect(url_for('admin.index'))

                
                return redirect(url_for('views.home'))  
            
            # if password is incorrect, flash error message
            else:
                flash("Incorrect password, please try again.",category='error')

        else:
            flash("User account does not exist, please create an account.",category="error")

    # if method is GET, render page
    return render_template('login.html',current_page="login",current_user=current_user)


# define route for logging out
@auth.route("/logout",methods=["GET"])
@login_required
def logout():
    logout_user()

    flash("Logged Out Successfully.",category="success")
    return redirect(url_for('auth.login',logout=True))


# define route for changing password
@auth.route('/change_password',methods=['GET','POST'])
@login_required
def change_password():
    if request.method == "POST":
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')

        if check_password_hash(current_user.password, old_password):
            current_user.password = generate_password_hash(new_password,method='scrypt')
            db.session.commit()
            flash('Password successfully changed.',category='success')
        
        else:
            db.session.rollback()
            flash("Incorrect old password.",category='error')
        

    return render_template('change_password.html',current_page='change_password')