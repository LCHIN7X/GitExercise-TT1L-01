from flask import Flask
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_login import LoginManager
from auth.models import db
from flask_msearch import Search
import os
from auth.views import auth
from admin import admin, add_admin_to_db

# ------------------------------- CODE ---------------------------------------------

DATABASE_NAME = "database.db"
bcrypt = Bcrypt()
search = Search(db=db)
photos = UploadSet("photos", IMAGES)


# Create function to create app instance

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_NAME}"
    app.config["UPLOADED_PHOTOS_DEST"] = "static/images"
    app.config["SECRET_KEY"] = os.urandom(24)
   
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

    from shbooks.views import shbooks 
    app.register_blueprint(shbooks,url_prefix="/shbooks")

  
    with app.app_context():
        db.create_all()
    
    
    add_admin_to_db(app)
    
    # create LoginManager object to handle logins
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)


    @login_manager.user_loader 
    def load_user(id):
        user = db.session.get(User, int(id))
        return user
    
    return app 



if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)