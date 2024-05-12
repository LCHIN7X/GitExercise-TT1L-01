from wtforms import Form, TextAreaField, validators
from flask_wtf.file import FileAllowed, FileRequired, FileField


class ProfilePictureForm(Form):
    image = FileField('Image',validators=[FileRequired(),FileAllowed('jpg','png',)])


class BioForm(Form):
    bio = TextAreaField("Bio",[validators.DataRequired()])