from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField,SubmitField
from wtforms.validators import DataRequired


class Editbook(FlaskForm):
   
    price = IntegerField('Price', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    submit = SubmitField('Submit')