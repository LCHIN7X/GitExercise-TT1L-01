from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from auth.models import db, User
from books.models import Addbook, Subject
from werkzeug.security import generate_password_hash

#  initialize Admin instance
admin = Admin(template_mode='bootstrap4')

#  add views for admin
admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Addbook,db.session))
admin.add_view(ModelView(Subject,db.session))


def add_admin_to_db(app):
    with app.app_context():
        email = "admin@gmail.com"
        username = "admin123"
        student_id = "super_user"
        password = "superuserdo123"

        admin_in_db = User.query.filter_by(email=email, 
                                           username=username,
                                           student_id=student_id).first()

        if not admin_in_db:
            admin_user = User(email=email,
                            username=username,
                            student_id=student_id,
                            password=generate_password_hash(password,method="scrypt"))
            db.session.add(admin_user)
            db.session.commit()
            print("Admin successfully added!")