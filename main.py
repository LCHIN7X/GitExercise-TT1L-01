from auth.models import db
from flask import Flask 
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_login import LoginManager
from admin import admin, add_admin_to_db
from flask_msearch import Search
import os

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
    app.config["UPLOADED_PHOTOS_DEST"] = "static/assets/images/user_uploads"
    configure_uploads(app, photos)

    from auth.models import User

    db.init_app(app)
    admin.init_app(app)
    search.init_app(app)

    #  registering flask Blueprints
    from auth.views import auth
    app.register_blueprint(auth, url_prefix="/auth")

    from books.views import views 
    app.register_blueprint(views, url_prefix="/views")
    
    from user.views import user
    app.register_blueprint(user,url_prefix="/user",name="user_bp")

    
    from books.models import Faculty, Subject, Book

    with app.app_context():
        db.create_all()

    add_admin_to_db(app)

    #  create LoginManager object to handle logins
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader 
    def load_user(id):
        user = db.session.get(User, int(id))
        print(user)
        return user
    
    return app 



if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)