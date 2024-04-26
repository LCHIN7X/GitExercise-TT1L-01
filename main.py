from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

# ------------------------------- CODE ---------------------------------------------

# Intialize SQLAlchemy database
database = SQLAlchemy()
DATABASE_NAME = "database.db"

# Create function to create app instance
def create_app():
    # create new Flask app and configuring app settings
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "wellofwisdom"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_NAME}"
    database.init_app(app)

    #  registering flask Blueprints
    from auth.views import auth
    app.register_blueprint(auth, url_prefix="/auth")

    with app.app_context():
        database.create_all()

    return app 

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)