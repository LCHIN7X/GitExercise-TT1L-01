from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView


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
    column_list = ['name','price','stock','desc','pub_date','faculty','subject']
    form_columns = ['name','price','stock','desc','pub_date','faculty','subject','image']
    column_filters = ['price','faculty','subject']
    column_searchable_list = ['name','desc']


class AdminUserView(AdminModelView):
    column_list = ['id','email','username','student_id']
    form_columns = ['email','username','student_id','password']
    column_filters = ['email','username','student_id']
    column_searchable_list = ['email','username','student_id']