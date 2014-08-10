from flask.ext.sqlalchemy import SQLAlchemy
from Crypto.Cipher import AES
import binascii

key = '0123456789abcdef'
"""The encryption key.   Random for this example."""

def aes_encrypt(data):
    cipher = AES.new(key)
    data = data + (" " * (16 - (len(data) % 16)))
    return binascii.hexlify(cipher.encrypt(data))

def aes_decrypt(data):
    cipher = AES.new(key)
    return cipher.decrypt(binascii.unhexlify(data)).rstrip()

db = SQLAlchemy()
 
class smarketers(db.Model):
  __tablename__ = 'smarketers'
  userID = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(255), unique=True)
  password = db.Column(db.String(255))
  firstName = db.Column(db.String(255))
   
  def __init__(self, username, password, firstName):
    self.username = username.lower()
    self.set_password(password)
    self.firstName = firstName.title()
     
  def set_password(self, password):
    self.password = aes_encrypt(password)
   
  def check_password_encrypt(self, password):
    return aes_encrypt(password) == self.password
