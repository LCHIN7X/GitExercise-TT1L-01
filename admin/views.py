from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import flash, redirect, url_for
from books.models import Book
from flask_admin.form.upload import FileUploadField
from wtforms.validators import InputRequired, ValidationError
from werkzeug.utils import secure_filename


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
    

class AdminBookView(AdminModelView):
    column_labels = {
        "name" : "Book Name",
        "faculty.name" : "Faculty",
        "subject.name" : "Subject",
        "desc" : "Description",
        "pub_date" : "Date Published"
    }
    column_list = ['name','price','stock','desc','pub_date','faculty','subject']
    form_columns = ['name','price','stock','desc','pub_date','faculty','subject','image','user']
    column_filters = ['name','faculty.name','subject.name','pub_date']
    column_sortable_list = ['name','price','stock','pub_date', ('faculty','faculty.name'), ('subject', 'subject.name')]
    column_searchable_list = ['name']

    form_extra_fields = {
        'image' : FileUploadField('Image',
                                  base_path="static/images", 
                                  relative_path="assets/images/",
                                  validators=[InputRequired()])
                        }

    
    def on_model_change(self, model, form, is_created):
        if is_created:
            model.user_id = current_user.id 
        model.user = current_user

    
    def validate_form(self, form):
        
        img_field = form.image
        if img_field.data:
            filename = secure_filename(img_field.data.filename)
            if not file_is_valid(filename):
                raise ValidationError('Invalid File Type: Only .jpg, .png and .jpeg Are Allowed.')
            
        return super().validate_form(form)    

    def on_validation_error(self, form):
        flash('Form validation failed',category='error')
        return redirect(url_for('admin.index'))


class AdminUserView(AdminModelView):
    column_labels = {
        'email' : "Email",
        "username" : "Username",
        "student_id" : 'Student ID',
        "is_admin" : "Is Admin"
    }
    column_list = ['email','username','student_id','is_admin']
    form_columns = ['email','username','student_id','password','is_admin']
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
    column_filters = ['email','username','student_id','is_admin']
    column_searchable_list = ['email','username','student_id','is_admin']



    def delete_model(self, model):
        if current_user == model:
            flash("You Cannot Delete Accounts That Are Active In Use.",category="error")
            return False

        if model.is_admin:
            flash("You Cannot Delete Admin Accounts.",category="error")
            return False

        return super().delete_model(model)