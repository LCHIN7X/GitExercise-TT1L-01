from flask_admin import Admin, AdminIndexView
from auth.models import db, User
from books.models import Book, Subject, Faculty
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from flask_login import current_user



class AdminIndex(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def can_edit(self):
        return True
    
    def can_delete(self):
        return True


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def can_edit(self):
        return True 
    
    def can_delete(self):
        return True
    

class AdminBookView(AdminModelView):
    column_list = ['name','price','stock','desc','pub_date','faculty','subject','image']
    form_columns = ['name','price','stock','desc','pub_date','faculty','subject','image']
    column_filters = ['price','faculty','subject']
    column_searchable_list = ['name','desc']


#  initialize Admin instance
admin = Admin(template_mode='bootstrap4',index_view=AdminIndex())

    
#  add views for admin
admin.add_view(AdminModelView(User,db.session))
admin.add_view(AdminBookView(Book,db.session))
admin.add_view(AdminModelView(Subject,db.session))
admin.add_view(AdminModelView(Faculty,db.session))

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
