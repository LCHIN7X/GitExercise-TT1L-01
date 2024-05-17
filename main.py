from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_login import LoginManager
from auth.models import db
from flask_msearch import Search

import os

# ------------------------------- CODE ---------------------------------------------
# Intialize SQLAlchemy database


# search = Search()
from auth.views import auth
from admin import admin, add_admin_to_db

# ------------------------------- CODE ---------------------------------------------

DATABASE_NAME = "database.db"
bcrypt = Bcrypt()
search = Search(db=db)
photos = UploadSet("photos", IMAGES)


# Create function to create app instance
def create_app():
    # create new Flask app and configuring app settings
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.urandom(24)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_NAME}"
    app.config["UPLOADED_PHOTOS_DEST"] = "static/images"
    app.config["SECRET_KEY"] = os.urandom(24)
   
    
    configure_uploads(app, photos)
    search.init_app(app)

    from auth.models import User
    
    db.init_app(app)
    admin.init_app(app)


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
    add_admin_to_db(app)
    
    # create LoginManager object to handle logins
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)


   
    @login_manager.user_loader 
    def load_user(id):
        user = db.session.get(User, int(id))
        print(user)
        return user
    
    return app 

# Get the Flask application instance


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)