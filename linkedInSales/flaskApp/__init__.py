from flask import Flask
from models import aes_decrypt
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = 'devkeythatencrypesthings'

toolbar = DebugToolbarExtension(app)

app.secret_key = app.config['SECRET_KEY']
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'YOUREMAIL@YOURDOMAIN.com'
app.config["MAIL_PASSWORD"] = aes_decrypt('YOUR ENCRYPTED PASSWORD HERE')

from routes import mail
mail.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:PASSWORD@localhost/DATABASE'

from models import db
db.init_app(app)

import flaskApp.routes
