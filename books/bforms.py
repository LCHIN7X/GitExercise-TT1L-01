from flask_wtf.file import FileAllowed,FileRequired,FileField
from wtforms import Form,IntegerField,StringField,TextAreaField,validators

class Addbooks(Form):
    name = StringField('Name',[validators.DataRequired()])
    price = IntegerField('Price',[validators.DataRequired()])
    stock = IntegerField('Stock',[validators.DataRequired()])
    discription = TextAreaField('Discription',[validators.DataRequired()])
    image = FileField('Image',validators=[FileRequired(),FileAllowed('jpg','png')])