# README #

This is CasperJS/PhantomJS with Firebase. A complete javascript solution.

### What is this repository for? ###

test.js is the program. It runs through linkedIn threads and creates messages to send to people. Currently, I want it to run through the first 10 people of the thread I already messaged and automatically submit them to our firebase database to make sure that works.

test-manual.html is a working example for submitting to our database using text fields.

test-retreive.html is a working example for retrieving all the userids in our database so our program can check against them before sending so we don't have an repeats.

### How do I get set up? ###

Download the latest vagrant build with:

vagrant box add precise32 https://dl.dropboxusercontent.com/u/3132018/linkedin-message.box

(or vagrant box add hashicorp/precise32 for a new one)

vagrant up
vagrant ssh
sudo apt-get install git
git clone https://USERNAMEHERE@bitbucket.org/dasickis/linkedin-sales-tool.git
sudo apt-get install python-pip
sudo pip install flask
sudo pip install SQLAlchemy
sudo apt-get update
sudo apt-get install apache2
sudo apt-get install mysql-server libapache2-mod-auth-mysql php5-mysql
sudo apt-get install php5 libapache2-mod-php5 php5-mcrypt
sudo apt-get install phpmyadmin
sudo pip install Flask-SQLAlchemy
sudo apt-get install python-dev
sudo pip install pycrypto
sudo pip install flask-wtf
sudo pip install flask-mail


Run the program with:

casperjs test.js

### Definitions

A Comment is:


A Conversation is:





### Network Diagram


1. Load Dash

                        Dash         Flask         DB  

                         ------------->
                         POST: /load_dash
                                      ------------->
                                        POST: Request
                                        <-------------
                                          [Listof Users],
                                          [Listof pitches],
                                          URLs, 
                                         # of ppl left per URL
                          <--------------
                           Users, pitches, URLs, 
                           # of ppl left per URL


2. Create Smarketer

                        Dash         Flask         DB
                       
                         ------------->
                          POST: /add_user
                           username, password, firstName
                                      ------------->
                                       ROUTE: 
                                        username, password, firstName
                                     <-------------  
                                      True  
          
                        <--------------  
                         True


3. Create Group

                        Dash         Flask         DB
                       
                         ------------->
                          POST: /add_group
                           groupID
                                      ------------->
                                       ROUTE: 
                                        groupID
                                     <-------------  
                                      True  
          
                        <--------------  
                         True

4. Create DiscussionThread

                        Dash         Flask         DB          Casper           LinkedIn

                         ------------->
                         POST: /goto_discussion
                               User
                               Discussion URL                 
                                       ----------->
                                        POST: /ask_pass
                                              User
                                       <----------
                                       First Name
                                       Pass
                                       -------------------->
                                       COMMAND LINE: import_discussion
                                       User
                                       Pass
                                       First Name
                                       Discussion URL
                                                              ----------------->
                                                              Login: User,Pass
                                                              <----------------
                                                                  Homepage

                                                              ----------------->
                                                              Goto: Discussion URL
                                                              <-----------------
                                                               Discussion page

                                                              ----------------->
                                                              Load More: comments
                                                              <-----------------
                                                               Additional comments

                                       <----------------------
                                       POST: /store_comments
                                             [Listof `comment`s]
                                       ----------->
                                       [Listof `comment`s]

5. Create Pitch

                        Dash         Flask         DB

                        -------------->
                        POST: /add_pitch  
                              Pitch  
                                     ------------->  
                                     POST: /store_pitch  
                                           Pitch  
                                     <-------------  
                                      True  
                        <--------------  
                         True


6. Send Pitch

                        Dash         Flask         DB          Casper           LinkedIn


                        -------------->
                        POST: /send_pitch  
                         Username
                         Password
                         First Name
                         Pitch
                         UserID
                         Group ID

                                     --------------->  
                                      # of messages to
                                     send, url
                                     <--------------
                                      [Listof userId]

                                     --------------->
                                        user
                                     <--------------
                                       pass

                                     ---------------------------->  
                                      Pitch, 
                                      User, 
                                      Pass, 
                                      Group Id,
                                      [Listof UserIds]
                                      <----------------------------
                                       POST: /store_successful
                                             [Listof UserIds]
                                       --------------->
                                        [listof userids],
                                        pitch

7. Create Reply

                        Dash         Flask         DB

                        -------------->
                        POST: /add_reply  
                        reply,
                        send profile url / user
                        recipient profile url / user 
                                     ------------->  
                                     POST: /store_reply  
                                     reply,
                                     send profile url / user
                                     recipient profile url / user 
                                     <-------------  
                                      True  
                        <--------------  
                         True
<<<<<<< HEAD
=======

#Database Diagram
* smarketers are us
* pitches are the automated pitches we are sending out
* groups are the linkedIn groups that we joined
* discussionThreads are the threads from the groups
* warehousePeople are the people are potential customers found from discussionThreads


* conversationStarters are the first message we send out. They send a Pitch from a smarketer to a warehousePeople.
* replies are messages sent after the initial message of a conversationStarter between a smarketer and a warehousePeople

![Screen Shot 2014-08-07 at 12.38.56 PM.png](https://bitbucket.org/repo/qAbGER/images/2154469389-Screen%20Shot%202014-08-07%20at%2012.38.56%20PM.png)
>>>>>>> 1a018486109a40cf25d90a4660945144eaf17ee4