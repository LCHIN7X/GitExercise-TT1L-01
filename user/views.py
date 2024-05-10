from flask import Blueprint, render_template, request

user = Blueprint('user',__name__,template_folder="templates",static_folder="static")


@user.route('/customize_profile', methods=["GET","POST"])
def customize_profile():

    

    return render_template('customize_profile.html',current_page="customize_profile")