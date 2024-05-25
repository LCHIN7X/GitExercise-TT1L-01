from flask_admin import Admin
from auth.models import db, User
from books.models import Book, Faculty, Subject
from books.invoice import Invoice
from werkzeug.security import generate_password_hash
from .views import AdminIndex, AdminBookView, AdminUserView, AdminModelView, AdminInvoiceView, BrandNewBookView, SecondHandBookView

#------------------------------------CODE-----------------------------------------------


#  initialize Admin instance
admin = Admin(template_mode='bootstrap4',index_view=AdminIndex())

    
#  add views for admin
admin.add_view(AdminBookView(Book,db.session, endpoint="all_books", name="All Books"))
admin.add_view(BrandNewBookView(Book,db.session, endpoint="brand_new_books", name="Brand New Books"))
admin.add_view(SecondHandBookView(Book,db.session, endpoint="second_hand_books",name="Second Hand Books"))
admin.add_view(AdminUserView(User,db.session))
admin.add_view(AdminModelView(Faculty,db.session))
admin.add_view(AdminModelView(Subject,db.session))
admin.add_view(AdminInvoiceView(Invoice,db.session))


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
