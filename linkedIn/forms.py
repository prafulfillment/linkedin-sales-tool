from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from models import db, smarketers
 
class ContactForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")

class SignupForm(Form):
  firstName = TextField("first name",  [validators.Required("Please enter your first name as you want it to appear in messages.")])
  username = TextField("Email",  [validators.Required("Please enter your linkedin login email address."), validators.Email("Please enter your linkedin login email address.")])
  password = PasswordField('Password', [validators.Required("Please enter your linkedin password.")])
  submit = SubmitField("Add new LinkedIn Account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = smarketers.query.filter_by(username = self.username.data.lower()).first()
    if user:
      self.username.errors.append("That account is already in the system.")
      return False
    else:
      return True

class SigninForm(Form):
  username = TextField("Email",  [validators.Required("Please enter your linkedin email address."), validators.Email("Please enter your linkedin email address.")])
  password = PasswordField('Password', [validators.Required("Please enter your linkedin password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = smarketers.query.filter_by(username = self.username.data.lower()).first()
    if user and user.check_password_encrypt(self.password.data):
      return True
    else:
      self.username.errors.append("Invalid e-mail or password")
      return False
