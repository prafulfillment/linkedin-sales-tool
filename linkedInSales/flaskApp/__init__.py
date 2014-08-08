from flask import Flask
from models import aes_decrypt

app = Flask(__name__)

app.secret_key = 'supersecretdevkey'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'james@derivatived.com'
app.config["MAIL_PASSWORD"] = aes_decrypt('64cb6dfee1a02d585a4eb9125458f3f2')

from routes import mail
mail.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:02cool4coldmessaging@localhost/linkedInSales'

from models import db
db.init_app(app)

import flaskApp.routes
