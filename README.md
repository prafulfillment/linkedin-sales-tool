# README #

This is CasperJS/PhantomJS with Firebase. A complete javascript solution.

### What is this repository for? ###

test.js is the program. It runs through linkedIn threads and creates messages to send to people. Currently, I want it to run through the first 10 people of the thread I already messaged and automatically submit them to our firebase database to make sure that works.

test-manual.html is a working example for submitting to our database using text fields.

test-retreive.html is a working example for retrieving all the userids in our database so our program can check against them before sending so we don't have an repeats.

### How do I get set up? ###

Download the latest vagrant build with:

1. vagrant box add precise32 https://dl.dropboxusercontent.com/u/3132018/linkedin-message.box (or vagrant box add hashicorp/precise32 for a new one)
 
2. vagrant up
 
3. vagrant ssh

4. sudo apt-get install git

5. git clone https://USERNAMEHERE@bitbucket.org/dasickis/linkedin-sales-tool.git

6. sudo apt-get install python-pip

7. sudo apt-get update

8. sudo apt-get install apache2 mysql-server libapache2-mod-auth-mysql php5-mysql php5 libapache2-mod-php5 php5-mcrypt phpmyadmin python-dev python-mysqldb vim

9. sudo pip install flask SQLAlchemy flask-mail flask-wtf pycrypto Flask-SQLAlchemy

10. exit

*In your terminal*

11. vim VagrantFile
  config.vm.network "forwarded_port", guest: 5000, host: 5000 
  config.vm.network "forwarded_port", guest: 80, host: 4999

12. vagrant reload

*Back in your vagrant

13. vagrant ssh

14. sudo ln -s /usr/share/phpmyadmin/ /var/www/phpmyadmin

15. sudo /etc/init.d/apache2 restart

*In the browser

16. Go to localhost:4999/phpmyadmin
create database called linkedInSales
click import database from dropbox/derivative/derivative

*In the vagrant again

17. cd linkedin-sales-tool/linkedInSales/

18. python runserver.py

*In the browser

19. Go to localhost:5000




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