from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from auth.models import db
from auth.views import auth
from app.views import home, add
from auth.models import db
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_login import LoginManager
from flask_msearch import Search

import os

# ------------------------------- CODE ---------------------------------------------

# Intialize SQLAlchemy database


DATABASE_NAME = "database.db"
bcrypt = Bcrypt()
search = Search()
photos = UploadSet("photos", IMAGES)

# Create function to create app instance
def create_app():
    # create new Flask app and configuring app settings
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "wellofwisdom"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_NAME}"
    app.config["UPLOADED_PHOTOS_DEST"] = "static/images"
    app.config["SECRET_KEY"] = os.urandom(24)
    configure_uploads(app, photos)
    db.init_app(app)
    search.init_app(app)

    # Registering flask Blueprints
    app.register_blueprint(auth, url_prefix="/auth")

    from books.views import views 
    app.register_blueprint(views, url_prefix="/views")
    
    
    from books.models import Faculty, Subject, Book

    with app.app_context():
        db.create_all()

    return app
    from auth.models import User

    #  create LoginManager object to handle logins
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader 
    def load_user(id):
        user = db.session.get(User, int(id))
        return user
    
    return app 

# Get the Flask application instance
app = create_app()

# Define route to render home template
@app.route('/')
def render_home():
    return render_template("base.html")

# Define route to render add template
@app.route('/add')
def render_add():
    return render_template("add.html")

if __name__ == "_main_":
    app.run(debug=True)