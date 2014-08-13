from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from models import db, Smarketer, Group, DiscussionThread, Pitch, Replies, ConversationStarters

class ContactForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")

class GroupForm(Form):
  groupID = TextField("groupID",  [validators.Required("Please enter the groupID")])
  title = TextField("title",  [validators.Required("Please enter the group title")])
  submit = SubmitField("Add a group")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False

    groupIDExists = Group.query.filter_by(groupID = self.groupID.data).first()
    if groupIDExists:
      self.groupID.errors.append("That group has already been added")
      return False
    else:
      return True

class PitchForm(Form):
  subject = TextField("subject",  [validators.Required("Please enter the subject")])
  message = TextAreaField("message",  [validators.Required("Please enter the message")])
  groupTitle = TextField("title",  [validators.Required("Please enter the title")])
  submit = SubmitField("Add a pitch")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    else:
      return True

class ConversationStartersForm(Form):
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
  
  def getAllPitchIDs():
    return Pitch.query.all()
  
  def getAllDiscussionThreadURLs():
    return DiscussionThread.query.all()
  
  submit = SubmitField("Send out pitches")
  discussionThreadURL = QuerySelectField("discussion threads", [validators.Required("Please select a valid discussion thread")], get_label="title",  query_factory=getAllDiscussionThreadURLs)
  pitchID = QuerySelectField("pitches", [validators.Required("Please select a valid pitch")], get_label="title",  query_factory=getAllPitchIDs)
  pitchNumber = TextField("# of ppl",  [validators.Required("Please enter a valid number")])
  
  def validate(self):
    if not Form.validate(self):
      return False

    pitchIDExists = Pitch.query.filter_by(pitchID = self.pitchID.data).first()
    if pitchIDExists:
      return True
    else:
      self.pitchID.errors.append("That pitch does not exist")
      return False  

    discussionThreadURLExists = DiscussionThread.query.filter_by(discussionThreadURL = self.url.data).first()
    if discussionThreadURLExists:
      return True
    else:
      self.discussionThreadURL.errors.append("That discussion thread does not exist")
      return False

    validPitches = WarehousePeople.query.filter_by(discussionURL = self.url.data, isPitched = false).count()
    pitchNumberValid <= validPitches
    if pitchNumberValid:
      return True
    else:
      self.pitchNumber.errors.append("Enter " + validPitches + " or less")
      return False
  
class DiscussionThreadForm(Form):
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def getAllGroupIDs():
    return Group.query.all()

  url = TextField("url",  [validators.Required("Please enter the url")]) 
  title = TextField("title",  [validators.Required("Please enter the title")])
  submit = SubmitField("Add a discussion thread")
  groupID = QuerySelectField("groupID", [validators.Required("Please select a valid groupID")], get_label="title",  query_factory=getAllGroupIDs)

  def validate(self):
    if not Form.validate(self):
      return False

    discussionThreadExists = DiscussionThread.query.filter_by(url = self.url.data).first()
    if discussionThreadExists:
      self.url.errors.append("That thread has already been added")
      return False

    groupIDExists = Group.query.filter_by(groupID = self.groupID.data).first()
    if groupIDExists:
      return True
    else:
      self.groupID.errors.append("That groupID does not exist")
      return False

class SignupForm(Form):
  firstName = TextField("First name",  [validators.Required("Please enter your first name.")])
  username = TextField("Email",  [validators.Required("Please enter your linkedIn email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter your linkedIn password.")])
  submit = SubmitField("Submit your linkedIn Account")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    
    user = Smarketer.query.filter_by(username = self.username.data.lower()).first()
    if user:
      self.username.errors.append("That account has already been created")
      return False
    else:
      return True

class SigninForm(Form):
  username = TextField("Email",  [validators.Required("Please enter your linkedIn email address."), validators.Email("Please enter your linkedIn email address.")])
  password = PasswordField('Password', [validators.Required("Please enter your linkedIn password.")])
  submit = SubmitField("Sign In")
  
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    
    user = Smarketer.query.filter_by(username = self.username.data).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.username.errors.append("Invalid e-mail or password")
      return False
