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

  def __init__(self, groupID):
    self.groupID = groupID

  def __str__(self):
    return str(self.groupID)

class DiscussionThread(db.Model):
  __tablename__ = 'discussionThreads'
  url = db.Column(db.String(767), primary_key = True)
  groupID = db.Column(db.Integer)

  def __init__(self, url, groupID):
    self.url = url
    self.groupID = groupID

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

