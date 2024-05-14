from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileRequired,FileField
from wtforms import Form,IntegerField,StringField,SubmitField
from wtforms.validators import DataRequired


class Editbook(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    image = FileField('Image',validators=[FileRequired(),FileAllowed('jpg','png',)])
    submit = SubmitField('Submit')
    
    
    # name = StringField('Name',[validators.DataRequired()])
    # price = IntegerField('Price',[validators.DataRequired()])
    # stock = IntegerField('Stock', [validators.DataRequired()])
    # image = FileField('Image',validators=[FileRequired(),FileAllowed('jpg','png',)])