from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_login import LoginManager
from auth.models import db

import os

# ------------------------------- CODE ---------------------------------------------
# Intialize SQLAlchemy database

DATABASE_NAME = "database.db"
bcrypt = Bcrypt()
photos = UploadSet("photos", IMAGES)

# Create function to create app instance
def create_app():
    # create new Flask app and configuring app settings
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "wellofwisdom"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_NAME}"
    app.config["UPLOADED_PHOTOS_DEST"] = "static/images"
    app.config["SECRET_KEY"] = os.urandom(24)
    db.init_app(app)
   
    
    configure_uploads(app, photos)


    #  registering flask Blueprints
    from auth.views import auth
    app.register_blueprint(auth, url_prefix="/auth")

    from books.views import views 
    app.register_blueprint(views, url_prefix="/views")
    
    from books.models import Faculty, Subject, Book
    from shbooks.views import shbooks 
    # Registering flask Blueprints
    # app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(shbooks,url_prefix="/")

    # from auth.models import db
    # from auth.models import User
    # from shbooks.models import SecondHandBooks


    with app.app_context():
        db.create_all()
    
    
    from auth.models import User


    return app

# Get the Flask application instance

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)