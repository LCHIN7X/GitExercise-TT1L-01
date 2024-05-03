from flask_admin import Admin
from auth.models import db, User
from books.models import Book, Subject
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from flask_login import current_user


#  initialize Admin instance
admin = Admin(template_mode='bootstrap4')


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
                            password=generate_password_hash(password,method="scrypt"),
                            is_admin=True)
            db.session.add(admin_user)
            db.session.commit()
            print("Admin successfully added!")


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    

#  add views for admin
admin.add_view(AdminModelView(User,db.session))
admin.add_view(AdminModelView(Book,db.session))
admin.add_view(AdminModelView(Subject,db.session))