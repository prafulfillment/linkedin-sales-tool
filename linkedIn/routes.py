from linkedIn import app
from flask import render_template, request, session, url_for, redirect, flash
from forms import ContactForm, SignupForm, SigninForm
from flask.ext.mail import Message, Mail
from models import db, smarketers, aes_decrypt

mail = Mail()
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'james@derivatived.com'
app.config["MAIL_PASSWORD"] = aes_decrypt('73802d433516575ec48b57615338c4e4')

mail.init_app(app)
 
@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')
 
@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='james@derivatived.com', recipients=['james@derivatived.com'])
      msg.body = """
      From: 
      Name: %s 
      Email: %s
      Message: %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
 
      return render_template('contact.html', success=True)
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@app.route('/dashboard')
def dashboard():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = smarketers.query.filter_by(username = session['email']).first()
 
  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('dashboard.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
 
  if 'email' in session:
    return redirect(url_for('dashboard')) 

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:   
      newuser = smarketers(form.username.data, form.password.data, form.firstName.data)
      db.session.add(newuser)
      db.session.commit()

      session['email'] = newuser.username
      return redirect(url_for('dashboard'))

  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
 
  if 'email' in session:
    return redirect(url_for('dashboard')) 
 
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.username.data
      return redirect(url_for('dashboard'))
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
     
  session.pop('email', None)
  return redirect(url_for('home'))
