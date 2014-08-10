from flask import Flask
 
app = Flask(__name__)      

app.secret_key = 'thisISaSECRETdevKEY!'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:02cool4coldmessaging@localhost/linkedInSales'
 
from models import db
db.init_app(app)

import linkedIn.routes
