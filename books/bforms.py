from flask_wtf.file import FileAllowed,FileRequired,FileField
from wtforms import Form,IntegerField,StringField,TextAreaField,validators
from wtforms.validators import  NumberRange


class Addbooks(Form):
    name = StringField('Name',[validators.DataRequired()])
    price = IntegerField('Price',[validators.DataRequired(), NumberRange(min=1)])
    stock = IntegerField('Stock',[validators.DataRequired(), NumberRange(min=1)])
    discription = TextAreaField('Discription',[validators.DataRequired()])
    condition = TextAreaField('Condition',[validators.DataRequired()])
    image = FileField('Image',validators=[FileRequired(),FileAllowed('jpg','png',)])