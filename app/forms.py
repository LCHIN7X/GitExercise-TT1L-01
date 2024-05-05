from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class AddBookForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    faculty = StringField('Faculty', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    remark = TextAreaField('Remark')
    submit = SubmitField('Add Book')