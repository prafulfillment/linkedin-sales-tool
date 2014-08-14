# README #

This is a CasperJS/PhantomJS-PHP/MySQL/Apache2-Flask/Jinja2/MySQL mess.

### What is this repository for? ###

This is the AUTOLINKER. A program to automatically send out messages to people on linkedIn.

### How do I get set up? ###

"In your terminal*

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

*back in your terminal outside of vagrant*

11. vim VagrantFile
  config.vm.network "forwarded_port", guest: 5000, host: 5000 
  config.vm.network "forwarded_port", guest: 80, host: 4999

12. vagrant reload

*Back in your vagrant*

13. vagrant ssh

14. sudo ln -s /usr/share/phpmyadmin/ /var/www/phpmyadmin

15. sudo /etc/init.d/apache2 restart

*In the browser*

16. Go to localhost:4999/phpmyadmin
create database called linkedInSales
click import database from dropbox/derivative/derivative

*In vagrant again*

17. git clone git://github.com/n1k0/casperjs.git
   
18. cd casperjs

19. sudo ln -sf `pwd`/bin/casperjs /usr/local/bin/casperjs

MAKE CASPERJS/PHANTOMJS WORK PRAFUL

20. cd linkedin-sales-tool/linkedInSales/

21. python runserver.py

*In the browser*

22. Go to localhost:5000




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
                          POST: /signup
                           username, password, firstName
                                      ------------->
                                       ROUTE: addSmarketer
                                        username, password, firstName
                                     <-------------  
                                      True  
          
                        <--------------  
                         True


3. Create Group

                        Dash         Flask         DB
                       
                         ------------->
                          POST: /addGroup
                           groupID, title
                                      ------------->
                                       ROUTE: addGroup
                                        groupID, title
                                     <-------------  
                                      True  
          
                        <--------------  
                         True

4. Create DiscussionThread

                        Dash         Flask         DB          Casper           LinkedIn

                         ------------->
                         POST: /addDiscussionThread
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
                        POST: /addPitch  
                              subject, message, title
                                     ------------->  
                                     ROUTE: addPitch 
                                           subject, message, title
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
                        POST: addReply  
                        message, fromWarehousePerson?,
                        fromSmarketer?, conversationStarterID
                                     ------------->  
                                     ROUTE: addReply
                                     message, fromWarehousePerson?,
                                     fromSmarketer?, conversationStarterID 
                                     <-------------  
                                      True  
                        <--------------  
                         True
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