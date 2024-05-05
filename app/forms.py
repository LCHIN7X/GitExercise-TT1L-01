from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, NumberRange


class AddBookForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    faculty = StringField('Faculty', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=0)])
    photo = FileField('Photo', validators=[DataRequired()])
    remark = TextAreaField('Remark')
    submit_add = SubmitField('Add Book')

class RemoveBookForm(FlaskForm):
    books = SelectField('Select book to remove:', validators=[DataRequired()], coerce=int)
    submit_remove = SubmitField('Remove Book')