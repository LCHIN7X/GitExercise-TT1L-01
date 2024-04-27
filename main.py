from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from auth.models import db
from auth.views import auth
from app.views import home, add

# Intialize SQLAlchemy database
DATABASE_NAME = "database.db"

# Create function to create app instance
def create_app():
    # create new Flask app and configuring app settings
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "wellofwisdom"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_NAME}"
    db.init_app(app)

    # Registering flask Blueprints
    app.register_blueprint(auth, url_prefix="/auth")

    with app.app_context():
        db.create_all()

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