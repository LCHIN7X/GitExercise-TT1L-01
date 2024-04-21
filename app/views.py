# imports
from flask import Blueprint, render_template 

# ------------------------------- CODE ---------------------------------------------

# Create new flask Blueprint with name "views"
views = Blueprint("views",__name__)

# NOTE: Incomplete! 
@views.route("/home")
def home():
    return render_template("base.html")