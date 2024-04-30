### from flask import Blueprint, render_template
from flask import Blueprint, render_template, url_for

views = Blueprint("views",__name__)

### Define the Blueprint with optional custom paths for templates and static files
views = Blueprint(
    "views",
    __name__,
    template_folder="templates",
    static_folder="static",  # Ensure this folder exists in your project
    static_url_path="/static/views"  # Optional custom path for Blueprint static files
)

### @views.route("/home")
@views.route("/")
def home():
    return render_template("base.html") 

@views.route("/add")
def add():
    return render_template("add-and-remove.html")