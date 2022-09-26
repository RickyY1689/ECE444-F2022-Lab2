from datetime import datetime
from xml.dom import ValidationErr
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, StopValidation

app = Flask(__name__)
app.config["SECRET_KEY"] = 'noonewillguessthis'

bootstrap = Bootstrap(app)
moment = Moment(app)

def validate_email(form, email):
    email_str = str(email.data)
    if email_str == '': return
    email_domain = email_str[email_str.find('@'):]
    if "utoronto" not in email_domain:
        raise StopValidation(email.gettext("Input a utoronto email address"))

class NameAndEmailForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField('What is your UofT email address?', validators=[DataRequired(), validate_email])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    email = None
    form = NameAndEmailForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
    form.name.data = ''
    form.email.data = ''
    return render_template('index.html', form=form, name=name, email=email)