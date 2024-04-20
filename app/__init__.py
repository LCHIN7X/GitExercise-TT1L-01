from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

database = SQLAlchemy()
DATABASE_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "wellofwisdom"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_NAME}"
    database.init_app(app)

    from .views import views 
    app.register_blueprint(views,url_prefix="/")

    with app.app_context():
        database.create_all()

    return app 