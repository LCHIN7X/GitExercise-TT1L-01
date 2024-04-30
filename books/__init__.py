from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads

import os

database = SQLAlchemy()
DATABASE_NAME = "database.db"
bcrypt = Bcrypt()
photos = UploadSet("photos", IMAGES)

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "wellofwisdom"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_NAME}"
    app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
    app.config["SECRET_KEY"] = os.urandom(24)
    configure_uploads(app, photos)
    database.init_app(app)

    from .views import views 
    app.register_blueprint(views,url_prefix="/")

    from .models import Faculty,Subject

    with app.app_context():
        database.create_all()

    return app 