# README #

This is a CasperJS/PhantomJS-PHP/MySQL/Apache2-Flask/Jinja2/MySQL mess.

### What is this repository for? ###

This is the AUTOLINKER. A program to automatically send out messages to people on linkedIn.

### How do I get set up? ###

**Import Vagrant**

```bash
# Import CasperJS box
$ vagrant box add precise32 https://dl.dropboxusercontent.com/u/3132018/linkedin-message.box (or vagrant box add hashicorp/precise32 for a new one)
$ vagrant init linkedin-message.box
$ vim VagrantFile
```

```vim
config.vm.network "forwarded_port", guest: 5000, host: 5000 
config.vm.network "forwarded_port", guest: 80, host: 4999
```

**Setup Vagrant**

```bash
$ vagrant reload
$ vagrant up
$ vagrant ssh

# Install LinkedIn-Sales-Tool pre-requisites
$ sudo apt-get update
$ sudo apt-get install apache2 mysql-server libapache2-mod-auth-mysql php5-mysql php5 libapache2-mod-php5 php5-mcrypt phpmyadmin python-dev python-mysqldb vim
$ sudo apt-get install python-pip
$ sudo apt-get install git
$ sudo pip install flask SQLAlchemy flask-mail flask-wtf pycrypto Flask-SQLAlchemy

# Setup PHPMyAdmin
$ sudo ln -s /usr/share/phpmyadmin/ /var/www/phpmyadmin
$ sudo /etc/init.d/apache2 restart

# Pull LinkedIn-Sales-Tool
$ git clone https://USERNAMEHERE@bitbucket.org/dasickis/linkedin-sales-tool.git

```

**In the browser**

http://localhost:4999/phpmyadmin

1. Create database called linkedInSales
2. Click import database from dropbox/derivative/derivative

**In vagrant again**

```bash
# Install PhantomJS pre-requisites
$ sudo apt-get install build-essential chrpath git-core libssl-dev libfontconfig1-dev

# Install PhantomJS
$ wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.7-linux-x86_64.tar.bz2
$ tar xvjf phantomjs-1.9.7-linux-x86_64.tar.bz2
$ sudo ln -s `pwd`/phantomjs-1.9.7-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs

# Install Casper
$ git clone git://github.com/n1k0/casperjs.git 
$ cd casperjs 
$ ln -sf `pwd`/bin/casperjs /usr/local/bin/casperjs
```

**Run LinkedIn-Sales-Tool**

```bash
$ python linkedInSales/runserver.py
```

http://localhost:5000

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
