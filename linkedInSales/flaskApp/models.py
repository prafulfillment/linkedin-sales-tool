from flask.ext.sqlalchemy import SQLAlchemy
from Crypto.Cipher import AES
import binascii

key = "123456789012345678901234"

def aes_encrypt(data):
    cipher = AES.new(key)
    data = data + (" " * (16 - (len(data) % 16)))
    return binascii.hexlify(cipher.encrypt(data))

def aes_decrypt(data):
    cipher = AES.new(key)
    return cipher.decrypt(binascii.unhexlify(data)).rstrip()

db = SQLAlchemy()

class ConversationStarters(db.Model):
  __tablename__ = 'conversationStarters'
  warehousePeopleID = db.Column(db.Integer, primary_key = True)
  smarketerPitched = db.Column(db.Integer)
  pitchID = db.Column(db.Integer)
  dateSent = db.Column(db.Date)
  connectionDistance = db.Column(db.Integer)
  isFirstDegree = db.Column(db.Boolean)
  isReplied = db.Column(db.Boolean)

  def __init__(self, smarketerPitched, pitchID, connectionDistance, isFirstDegree, isReplied):
    self.smarketerPitched = smarketerPitched
    self.pitchID = pitchID
    self.connectionDistance = connectionDistance
    self.isFirstDegree = isFirstDegree
    self.isReplied = isReplied

class Smarketer(db.Model):
  __tablename__ = 'smarketers'
  userID = db.Column(db.Integer, primary_key = True)
  firstName = db.Column(db.String(255))
  username = db.Column(db.String(255), unique=True)
  password = db.Column(db.String(255))
  
  def __init__(self, firstName, username, password):
    self.firstName = firstName.title()
    self.username = username.lower()
    self.set_password(password)
    
  def set_password(self, password):
    self.password = aes_encrypt(password)
  
  def check_password(self, password):
    return password == aes_decrypt(self.password)

class Group(db.Model):
  __tablename__ = 'groups'
  groupID = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(255))

  def __init__(self, groupID, title):
    self.groupID = groupID
    self.title = title

  def __str__(self):
    return str(self.groupID)

class DiscussionThread(db.Model):
  __tablename__ = 'discussionThreads'
  url = db.Column(db.String(767), primary_key = True)
  groupID = db.Column(db.Integer)
  title = db.Column(db.String(255))

  def __init__(self, url, groupID, title):
    self.url = url
    self.groupID = groupID
    self.title = title

class Replies(db.Model):
  __tablename__ = 'replies'
  replyID = db.Column(db.Integer, primary_key = True)
  conversationStarterID = db.Column(db.Integer)
  fromSmarketer = db.Column(db.Boolean)
  fromWarehousePeople = db.Column(db.Boolean)
  message = db.Column(db.Text)

  def __init__(self, conversationStarterID, fromSmarketer, fromWarehousePeople, message):
    self.conversationStarterID = conversationStarterID
    self.fromSmarketer = fromSmarketer
    self.fromWarehousePeople = fromWarehousePeople
    self.message = message

class WarehousePeople(db.Model):
  __tablename__ = 'warehousePeople'  
  warehousePeopleID = db.Column(db.Integer, primary_key = True)
  userID = db.Column(db.Integer)
  firstName = db.Column(db.String(255))
  lastName = db.Column(db.String(255))
  byline = db.Column(db.String(255))
  discussionURL = db.Column(db.String(767))
  comment = db.Column(db.Text)
  likesCount = db.Column(db.Integer)
  profileURL = db.Column(db.String(255))
  imageURL = db.Column(db.String(255))

  def __init__(self, userID, firstName, lastName, byline, discussionURL, comment, likesCount, profileURL, imageURL):
    self.userID = userID
    self.firstName = firstName
    self.lastName = lastName
    self.byline = byline
    self.discussionURL = discussionURL
    self.comment = comment
    self.likesCount = likesCount
    self.profileURL = profileURL
    self.imageURL = imageURL

class Pitch(db.Model):
  __tablename__ = 'pitches'
  pitchID = db.Column(db.Integer, primary_key = True)
  subject = db.Column(db.String(255))
  message = db.Column(db.Text)

  def __init__(self, subject, message):
    self.subject = subject
    self.message = message
