from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from models import db, Smarketer, Group, DiscussionThread, Pitch, Replies, ConversationStarters, WarehousePeople

class ContactForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")

class GroupForm(Form):
  groupID = TextField("groupID",  [validators.Required("Please enter the groupID")])
  groupTitle = TextField("title",  [validators.Required("Please enter the group title")])
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
    
    return True

class PitchForm(Form):
  subject = TextField("subject",  [validators.Required("Please enter the subject")])
  message = TextAreaField("message",  [validators.Required("Please enter the message")])
  pitchTitle = TextField("title",  [validators.Required("Please enter the title")])
  submit = SubmitField("Add a pitch")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    
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
    if pitchIDExists == False:
      self.pitchID.errors.append("That pitch does not exist")
      return False  

    discussionThreadURLExists = DiscussionThread.query.filter_by(url = self.discussionThreadURL).first()
    if discussionThreadURLExists == False:
      self.discussionThreadURL.errors.append("That discussion thread does not exist")
      return False

    validPitches = WarehousePeople.query.filter_by(discussionURL = self.discussionThreadURL.data, isPitched = False).count()
    pitchNumberValid = int(self.pitchNumber.data) <= validPitches
    if pitchNumberValid == False:
      self.pitchNumber.errors.append("Enter " + str(validPitches) + " or less. You entered "+ str(self.pitchNumber.data))
      return False

    return True 
  
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
    if groupIDExists == False:
      self.groupID.errors.append("That groupID does not exist")
      return False

    return True

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
    if (user == False) and (user.check_password(self.password.data) == False):
      self.username.errors.append("Invalid e-mail or password")
      return False
    
    return True
