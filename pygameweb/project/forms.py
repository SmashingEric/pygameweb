from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired

from wtforms.fields import StringField, HiddenField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea



class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    tags = StringField('Tags')
    summary = StringField('Summary', widget=TextArea(), validators=[DataRequired()])
    description = StringField('Description', widget=TextArea())
    uri = URLField('Home URL', validators=[DataRequired()])

    image = FileField('image', validators=[
        # FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])

class ReleaseForm(FlaskForm):
    version = StringField('version', validators=[DataRequired()])
    description = StringField('description', widget=TextArea())
    srcuri = URLField('Source URL')
    winuri = URLField('Windows URL')
    macuri = URLField('Mac URL')



class FirstReleaseForm(ProjectForm, ReleaseForm):
    """Is for when the first release is being made.
    """



class ProjectCommentForm(FlaskForm):
    """ is for commenting on projects.
    """
    message = StringField('message', widget=TextArea())
    parent_id = HiddenField('parent_id')
    thread_id = HiddenField('thread_id')
