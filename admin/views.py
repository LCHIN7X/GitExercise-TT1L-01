from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import flash, redirect, url_for, request
from books.models import Book
from flask_admin.form.upload import FileUploadField
from wtforms.validators import InputRequired, ValidationError
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

#------------------------------------CODE-----------------------------------------------

def file_is_valid(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'png', 'jpeg'}

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
    
    def can_create(self):
        return True

class AdminBookView(ModelView):
    column_labels = {
        "name": "Book Name",
        "faculty.name": "Faculty",
        "subject.name": "Subject",
        "desc": "Description",
        "pub_date": "Date Published",
        'con': 'Condition'
    }
    column_list = ['name', 'price', 'stock', 'desc', 'con', 'pub_date', 'faculty', 'subject']
    form_columns = ['name', 'price', 'stock', 'desc', 'con', 'pub_date', 'faculty', 'subject', 'image', 'user']
    column_filters = ['name', 'faculty.name', 'subject.name', 'pub_date']
    column_sortable_list = ['name', 'price', 'stock', 'pub_date', ('faculty', 'faculty.name'), ('subject', 'subject.name')]
    column_searchable_list = ['name']

    form_extra_fields = {
        'image': FileUploadField('Image',
                                 base_path="static/images",
                                 relative_path="assets/images/",
                                 validators=[InputRequired()])
    }

    form_args = {
        'con': {
            'default': 'Brand New'
        }
    }

    def create_model(self, form):
        try:
            print(f"create_model called for book: {form.name.data}")
            book_name = form.name.data
            book_already_exists = Book.query.filter_by(name=book_name).first()
            print(f"Query result for book with name '{book_name}': {book_already_exists}")

            model = self.model()
            form.populate_obj(model)

            if book_already_exists:
                print(f"Book with name '{book_name}' already exists.")
                model.is_original = False
            else:
                print(f"No book with name '{book_name}' found. Setting is_original to True.")
                model.is_original = True

            model.user_id = current_user.id
            model.user = current_user

            self.session.add(model)
            self.session.commit()
            return model

        except Exception as e:
            flash(f'Error creating book: {str(e)}', 'error')
            self.session.rollback()
            return False

    def validate_form(self, form):
        if hasattr(form, 'image'):
            img_field = form.image
            if img_field.data and hasattr(img_field.data, 'filename'):
                filename = secure_filename(img_field.data.filename)
                if not file_is_valid(filename):
                    raise ValidationError('Invalid File Type: Only .jpg, .png and .jpeg Are Allowed.')

        return super().validate_form(form)

    def on_validation_error(self, form):
        flash('Form validation failed', category='error')
        return redirect(url_for('admin.index'))


class BrandNewBookView(AdminBookView):
    def get_query(self):
        return super().get_query().filter_by(con="Brand New")

    def get_count_query(self):
        return super().get_count_query().filter_by(con="Brand New")
    

class SecondHandBookView(AdminBookView):
    def get_query(self):
        return super().get_query().filter(Book.con != "Brand New")

    def get_count_query(self):
        return super().get_count_query().filter(Book.con != "Brand New")
    
    def can_create(self):
        return False 
    
    def can_edit(self):
        return False 
    
    def can_delete(self):
        return False
    
    def create_model(self, form):
        flash("Only Non-Admins can add secondhand books.",category='error')
        return False 
    
    def update_model(self, form):
        flash("You Cannot Update Details of Secondhand Books",category='error')
        return False 
    
    def delete_model(self, form):
        flash("You Cannot Delete Secondhand Books.",category='error')
        return False
    

class AdminUserView(AdminModelView):
    column_labels = {
        'email': "Email",
        "username": "Username",
        "student_id": 'Student ID',
        "is_admin": "Is Admin"
    }
    column_list = ['email', 'username', 'student_id', 'is_admin']
    form_columns = ['email', 'username', 'student_id', 'password', 'is_admin']
    form_edit_rules = [
        'email',
        'username',
        'student_id',
        'is_admin'
    ]
    form_create_rules = [
        'email',
        'username',
        'student_id',
        'password',
        'is_admin'
    ]
    column_filters = ['email', 'username', 'student_id', 'is_admin']
    column_searchable_list = ['email', 'username', 'student_id', 'is_admin']

    def create_model(self, form):
        password = form.password.data
        hashed_password = generate_password_hash(password, method="scrypt")
        form.password.data = hashed_password

        return super().create_model(form)

    def delete_model(self, model):
        if current_user == model:
            flash("You Cannot Delete Accounts That Are Active In Use.", category="error")
            return False

        if model.is_admin:
            flash("You Cannot Delete Admin Accounts.", category="error")
            return False

        return super().delete_model(model)


class AdminInvoiceView(AdminModelView):
    def can_delete(self):
        return False
    
    def can_create(self):
        return False
    
    column_labels = {
        "user.username" : "Username",
        'invoice' : "Invoice ID",
        "status" : 'Payment Status',
        "date_order" : "Order Date"
    }
    column_list = ['user', 'invoice', 'status', 'date_order']
    form_columns = ['status']
    column_filters = ['status', 'invoice', 'date_order', 'user.username']
    column_searchable_list = ['status', 'invoice', 'user.username']
    column_sortable_list = ['status', 'invoice', 'date_order', 'user.username']

    def _format_username(view, context, model, name):
        return model.user.username

    column_formatters = {
        'user': _format_username
    }