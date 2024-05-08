from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileAllowed,FileRequired,FileField


class AddBookForm(FlaskForm):
    student_id = IntegerField('student_id', validators=[DataRequired()])
    faculty = StringField('Faculty', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=0)])
    photo = FileField('photo',validators=[FileRequired(),FileAllowed('jpg','png')])
    remark = TextAreaField('Remark', validators=[DataRequired()])
    submit_add = SubmitField('Add Book')

class RemoveBookForm(FlaskForm):
    books = SelectField('Select book to remove:', validators=[DataRequired()], coerce=int)
    submit_remove = SubmitField('Remove Book')