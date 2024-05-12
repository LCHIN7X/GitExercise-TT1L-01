from flask import Blueprint, render_template, request, flash, redirect, url_for
from auth.models import db
from flask_login import current_user
from werkzeug.utils import secure_filename
from PIL import Image
import os

user = Blueprint('user',__name__,template_folder="templates",static_folder="static")


def file_is_valid(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'png', 'jpeg'}


@user.route('/customize_profile', methods=["GET","POST"])
def customize_profile():
    if request.method == "POST":
        
        if 'profile_pic' in request.files:
            profile_pic = request.files['profile_pic']
            
            if profile_pic.filename != "":
                if not file_is_valid(profile_pic.filename):
                    flash("Invalid File Type: Only .jpg, .jpeg and .png Files Are Allowed.",category="error")
                
                else:
                    cwd = os.getcwd()

                    #  if user's original pic is not the default, delete it
                    previous_profile_pic = current_user.profile_pic
                    if previous_profile_pic != "default_pfp.png":
                        os.remove(f"{cwd}/user/static/assets/images/user_uploads/{previous_profile_pic}")

                    filename = secure_filename(profile_pic.filename)
                    os.makedirs(f"{cwd}/user/static/assets/images/user_uploads", exist_ok=True)

                    # resize image (make image smaller so it takes up less space) 
                    img_size = (250,250)
                    i = Image.open(profile_pic)
                    i.thumbnail(img_size)

                    i.save(os.path.join(f"{cwd}/user/static/assets/images/user_uploads", filename))
                    current_user.profile_pic = filename
                    db.session.commit()
                    flash("Profile Picture Successfully Updated!",category='success')

        bio = request.form.get('bio')
        
        if bio is not None and bio.strip() != "":
            current_user.bio = bio 
            db.session.commit()
            flash("Bio Successfully Updated!",category='success')
            return redirect(url_for('user_bp.customize_profile'))
        
        else:
            current_user.bio = None 
            db.session.commit()
            flash("Bio Successfully Cleared!",category="success")
            return redirect(url_for('user_bp.customize_profile'))


    current_bio = current_user.bio
    current_profile_pic = current_user.profile_pic 
    return render_template('customize_profile.html',
                           current_page="customize_profile",
                           current_profile_pic=current_profile_pic,
                           current_bio=current_bio)