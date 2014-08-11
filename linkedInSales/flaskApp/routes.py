from flaskApp import app
from flask import render_template, request, flash, session, url_for, redirect
from forms import ContactForm, SignupForm, SigninForm, GroupForm, DiscussionThreadForm
from flask.ext.mail import Message, Mail
from models import db, Smarketer, Group, DiscussionThread, aes_decrypt
from subprocess import check_output

mail = Mail()

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
      msg = Message(form.subject.data, sender='contact@derivatived.com', recipients=['james@derivatived.com'])
      msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)

      return render_template('contact.html', success=True)

  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()

  if 'email' in session:
    return redirect(url_for('profile')) 
  
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = Smarketer(form.firstName.data, form.username.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()
      
      session['email'] = newuser.username
      return redirect(url_for('profile'))
  
  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@app.route('/profile')
def profile():

  if 'email' not in session:
    return redirect(url_for('signin'))

  user = Smarketer.query.filter_by(username = session['email']).first()

  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('profile.html')

@app.route('/addGroup', methods=['GET', 'POST'])
def addGroup():
  
  if 'email' not in session:
    return redirect(url_for('signin'))

  user = Smarketer.query.filter_by(username = session['email']).first()

  if user is None:
    return redirect(url_for('signin'))
  else:
    form = GroupForm()
    
    if request.method == 'POST':
      if form.validate() == False:
        return render_template('addGroup.html', form=form)
      else:
        newGroup = Group(form.groupID.data)
        db.session.add(newGroup)
        db.session.commit()
       
        form.groupID.data = ""
        return render_template('addGroup.html', form=form)

    elif request.method == 'GET':
      return render_template('addGroup.html', form=form)  
  
@app.route('/addDiscussionThread', methods=['GET', 'POST'])
def addDiscussionThread():

  if 'email' not in session:
    return redirect(url_for('signin'))

  user = Smarketer.query.filter_by(username = session['email']).first()

  if user is None:
    return redirect(url_for('signin'))
  else:
    form = DiscussionThreadForm()

    if request.method == 'POST':
      if form.validate() == False:
        return render_template('addDiscussionThread.html', form=form)

      else:
	#TODO throws error somehow, when it hits casper?
	# test with group id 4117360 and url https://www.linkedin.com/groups/Safety-productivity-accuracy-please-rank-4117360.S.5828896882205683713?view=&item=5828896882205683713&type=member&gid=4117360&trk=eml-b2_anet_digest-group_discussions-14-grouppost-disc-2&midToken=AQFwAv_iTaBQJA&fromEmail=fromEmail&ut=26E3RCSJJaHSk1
        usernameText = "--username='" + user.username + "'"
        passwordText = "--password='" + aes_decrypt(user.password) + "'"
        firstNameText = "--first-name='" + user.firstName + "'"
        discussionURLText = "--discussion-url='" + form.url.data + "'"
        out = check_output(["casperjs", "linkedin-sales.js", usernameText, passwordText, firstNameText, discussionURLText])

	#TODO subprocess.open()

	#saves new discussionThread in database
        newDiscussionThread = DiscussionThread(form.url.data, form.groupID.data)
        db.session.add(newDiscussionThread)
        db.session.commit()

        form.url.data = ""
        return render_template('addDiscussionThread.html', form=form)

    elif request.method == 'GET':
      return render_template('addDiscussionThread.html', form=form)
  
@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()

  if 'email' in session:
    return redirect(url_for('profile')) 
      
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.username.data
      return redirect(url_for('profile'))
                
  elif request.method == 'GET':
    return render_template('signin.html', form=form)

@app.route('/signout')
def signout():

  if 'email' not in session:
    return redirect(url_for('signin'))
    
  session.pop('email', None)
  return redirect(url_for('home'))
