from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from auth.models import db, User
from books.models import Addbook, Subject

#  initialize Admin instance
admin = Admin(template_mode='bootstrap4')

#  add views for admin
admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Addbook,db.session))
admin.add_view(ModelView(Subject,db.session))