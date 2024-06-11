from flask_login import current_user, logout_user
from flask_admin import AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask import flash, redirect, url_for, request, render_template_string
from books.models import Book, BannedBook
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
            book_name = form.name.data
            book_condition = form.con.data
            book_already_exists = Book.query.filter_by(name=book_name).first()
            book_is_banned = BannedBook.query.filter_by(book_name=book_name.lower()).first()

            model = self.model()
            #  prepopulate value in form_args (con)
            form.populate_obj(model)

            if book_is_banned:
                self.session.rollback()
                flash(f"Unable to add book with title of {book_name} because it is banned by the system.",category="error")    
                return False 

            if book_condition != "Brand New":
                self.session.rollback()
                flash("Admins cannot add second hand books.", category='error')
                return False
                
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
            flash(f'Error creating book: {str(e)}', category='error')
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
        return False
    
    def delete_model(self, model):
        return redirect(url_for('.confirm_delete_view',id=model.id))
    
    @expose('/delete/',methods=['GET','POST'])
    def delete_view(self):
        id_ = request.form.get('id')
        if id_:
            return redirect(url_for('.confirm_delete_view',id=id_))
        flash('No ID provided for deletion.',category='error')
        return redirect(url_for('.index_view'))


    @expose('/confirm_delete/', methods=['GET', 'POST'])
    def confirm_delete_view(self):
        if request.method == "POST":
            if request.form.get('confirm') == "yes":
                return self._delete_model()
            else:
                flash("Book deletion cancelled",category='error')
                return redirect(url_for('.index_view'))

        else:
            # get ID of entry to be deleted
            model_id = request.args.get('id')
            # render delete confirmation page
            return render_template_string('''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
                          rel="stylesheet"
                          integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
                          crossorigin="anonymous"
                    />
                    <title>Confirm Delete</title>
                </head>
                <body>
                <div style="text-align: center; margin-top: 50px;">
                    <h3>Are you sure you want to delete this book? This will delete all entries of the same book, and the book will be banned.</h3>
                    <form method="post" action='{{ url_for(".confirm_delete_view") }}'>
                        <input type="hidden" name="id" value="{{ model_id }}">
                        <button type="submit" name="confirm" value="yes" class='btn btn-primary mr-2'>Continue</button>
                        <button type="submit" name="confirm" value="no" class='btn btn-danger ml-2'>Cancel</button>
                    </form>
                </div>
                </body>
                </html>
            ''', model_id=model_id)


    def _delete_model(self):
        try:
            # get ID of entry to be deleted
            model_id = request.form.get('id')

            if not model_id:
                flash('ID not found.', category='error')
                return redirect(url_for('admin.index'))

            model = self.session.query(self.model).get(model_id)
            if model:
                
                new_banned_book = BannedBook(book_name=model.name.lower(),reason="Deleted by Admin")
                self.session.add(new_banned_book)
                self.session.delete(model)
                self.session.commit()
                flash('Book successfully deleted and banned!', category="success")

            else:
                flash("Unable to delete book.", category='error')


        except Exception as e:
            flash(f'Error occurred: {e}', category='error')
            self.session.rollback()

        return redirect(url_for('.index_view'))


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
        return True

    def create_model(self, form):
        flash("Only Non-Admins can add secondhand books.", category='error')
        return False

    def update_model(self, form, model):
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

class AdminFacultyView(AdminModelView):

    form_columns = ['name']

    def delete_model(self, model):
        if Book.query.filter_by(faculty_id=model.id).first():
            flash("Cannot delete faculty because it is linked to one or more books.", category='error')
            return False
        return super().delete_model(model)


class AdminSubjectView(AdminModelView):

    form_columns = ['name']

    def delete_model(self, model):
        if Book.query.filter_by(subject_id=model.id).first():
            flash("Cannot delete subject because it is linked to one or more books.", category='error')
            return False
        return super().delete_model(model)


class AdminLogoutView(BaseView):
    @expose('/')
    def logout_admin(self):
        logout_user()
        flash("Logged Out Successfully!", category='success')
        return redirect(url_for('auth.login'))