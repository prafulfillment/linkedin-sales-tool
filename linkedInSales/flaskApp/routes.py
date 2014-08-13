from flaskApp import app
from flask import render_template, request, flash, session, url_for, redirect, jsonify
from forms import ContactForm, SignupForm, SigninForm, GroupForm, DiscussionThreadForm, PitchForm
from flask.ext.mail import Message, Mail
from models import db, Smarketer, Group, DiscussionThread, aes_decrypt, WarehousePeople, Pitch, ConversationStarters, Replies
import subprocess
import json
import os

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
	totalTitle = form.title.data + " - " + form.groupID.data
        newGroup = Group(form.groupID.data, totalTitle)
        db.session.add(newGroup)
        db.session.commit()

        return render_template('addGroup.html', success=True)

    elif request.method == 'GET':
      return render_template('addGroup.html', form=form)

@app.route('/addPitch', methods=['GET', 'POST'])
def addPitch():

  if 'email' not in session:
    return redirect(url_for('signin'))

  user = Smarketer.query.filter_by(username = session['email']).first()

  if user is None:
    return redirect(url_for('signin'))
  else:
    form = PitchForm()

    if request.method == 'POST':
      if form.validate() == False:
        return render_template('addPitch.html', form=form)
      else:
        newPitch = Pitch(form.subject.data, form.message.data)
        db.session.add(newPitch)
        db.session.commit()

        return render_template('addPitch.html', success=True)

    elif request.method == 'GET':
      return render_template('addPitch.html', form=form)

@app.route('/sendPitch', methods=['POST'])
def sendPitch():
    # TODO: Create a form for the remaining fields
    user = Smarketer.query.filter_by(username = session['email']).first()
    script_path = os.path.abspath('./flaskApp')
    commands = ['casperjs {}/linkedin-sales.js'.format(script_path)]
    commands.append("--user='{}'".format( user.username ))
    commands.append("--pass='{}'".format( aes_decrypt(user.password) ))
    commands.append("--first-name='{}'".format( user.firstName ))
    commands.append("--cookies-file='{}-cookies.txt'".format( user.firstName ))
    commands.append("--to-user-id=")
    commands.append("--pitch-subject=")
    commands.append("--pitch-body=")
    commands.append("--group-id=")
    commands.append("--send-pitch={}".format((not DEBUG)))
    command = " ".join(commands)
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = proc.communicate()

@app.route('/addDiscussionThread', methods=['GET', 'POST'])
def addDiscussionThread():

  if 'email' not in session:
    return redirect(url_for('signin'))

  user = Smarketer.query.filter_by(username = session['email']).first()
  savedDiscussionThread = False

  def saveDiscussionThread():
    #saves new discussionThread in database
    newDiscussionThread = DiscussionThread(form.url.data, form.groupID.data, form.title.data)
    db.session.add(newDiscussionThread)
    db.session.commit()
    savedDiscussionThread = True


  if user is None:
    return redirect(url_for('signin'))
  else:
    form = DiscussionThreadForm()

    if request.method == 'POST':
      if form.validate() == False:
        return render_template('addDiscussionThread.html', form=form)

      else:
        script_path = os.path.abspath('./flaskApp')
        commands = ['casperjs {}/linkedin-sales.js'.format(script_path)]
        commands.append("--user='{}'".format( user.username ))
        commands.append("--pass='{}'".format( aes_decrypt(user.password) ))
        commands.append("--first-name='{}'".format( user.firstName ))
        commands.append("--cookies-file='{}-cookies.txt'".format( user.firstName ))
        commands.append("--discuss-url='{}'".format( form.url.data ))
        command = " ".join(commands)
        proc = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        output = proc.communicate()
        try:
            comments = json.loads(output[0])
        except:
            comments = output[0]
            err = 'CasperJS timed out'
            print err
            response = jsonify(msg=err)
            return render_template('addDiscussionThread.html', isError=True, error=response, form=form)

        for c in comments:
            userID = c["userID"]
            name = c["name"]
            firstName = c["fname"]
            lastName = c["lname"]
            byline = c["byline"]
            userID = c["userID"]
            discussionURL = form.url.data
            likesCount = c["likes"]
            profileURL = c["profileURL"]
            isFirstDegree = c["isFirstDegree"]
            connection = c["connection"]
            imageURL = c["image_src"]
            comment = c["comment"]

            #saves new warehousePerson to database
            newWarehousePerson = WarehousePeople(userID, firstName, lastName, byline, discussionURL, comment, likesCount, profileURL, imageURL)

	    if savedDiscussionThread == False:
              saveDiscussionThread()

            db.session.add(newWarehousePerson)

        db.session.commit()

	if savedDiscussionThread:
	  return render_template('addDiscussionThread.html', success=savedDiscussionThread)

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
