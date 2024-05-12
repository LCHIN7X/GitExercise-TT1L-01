from flask import Blueprint, render_template, request, flash, redirect, url_for
from auth.models import db
from flask_login import current_user
from werkzeug.utils import secure_filename
import os

user = Blueprint('user',__name__,template_folder="templates",static_folder="static")


def file_is_valid(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'png', 'jpeg'}


@user.route('/customize_profile', methods=["GET","POST"])
def customize_profile():
    
    if request.method == "POST":
        bio = request.form.get('bio')

        if 'profile_pic' in request.files:
            profile_pic = request.files['profile_pic']
            
            if profile_pic.filename != "":
                if not file_is_valid(profile_pic.filename):
                    flash("Invalid File Type: Only .jpg, .jpeg and .png Files Are Allowed.",category="error")
                
                else:
                    filename = secure_filename(profile_pic.filename)
                    cwd = os.getcwd()
                    os.makedirs(f"{cwd}/user/static/assets/images/user_uploads", exist_ok=True)
                    profile_pic.save(os.path.join(f"{cwd}/user/static/assets/images/user_uploads", filename))
                    current_user.profile_pic = filename
                    db.session.commit()

        
        if bio:
            current_user.bio = bio 
            db.session.commit()
            flash("Account details successfully updated!", category='success')
            return redirect(url_for('user_bp.customize_profile'))


    current_bio = current_user.bio
    current_profile_pic = current_user.profile_pic 
    return render_template('customize_profile.html',
                           current_page="customize_profile",
                           current_profile_pic=current_profile_pic,
                           current_bio=current_bio)