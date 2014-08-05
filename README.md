# README #

This is CasperJS/PhantomJS with Firebase. A complete javascript solution.

### What is this repository for? ###

test.js is the program. It runs through linkedIn threads and creates messages to send to people. Currently, I want it to run through the first 10 people of the thread I already messaged and automatically submit them to our firebase database to make sure that works.

test-manual.html is a working example for submitting to our database using text fields.

test-retreive.html is a working example for retrieving all the userids in our database so our program can check against them before sending so we don't have an repeats.

### How do I get set up? ###

Download the latest vagrant build with:

vagrant box add https://dl.dropboxusercontent.com/u/3132018/linkedin-message.box

Run the program with:

casperjs test.js

### Definitions

A Comment is:


A Conversation is:





### Network Diagram


1. Load Dash

                        Dash         Flask         DB  

                         ------------->
                           Request
                                      ------------->
                                        Request
                                        <-------------
                                          Users, pitches,
                                          URLs, # of ppl left per URL
                          <--------------
                           Users, pitches, URLs, 
                           # of ppl left per URL


2. Create User

                        Dash         Flask         DB
                       
                         ------------->
                           User, pass
                                      ------------->
                                        user/ pass
                                     <-------------  
                                      True  
          
                        <--------------  
                         True

3. Import Discussion

                        Dash         Flask         DB          Casper           LinkedIn

                         ------------->
                         POST: /goto_discussion
                               User
                               Discussion URL                 
                                       ----------->
                                        POST: /ask_pass
                                              User
                                       <----------
                                       Pass
                                       -------------------->
                                       User, Pass
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
                                         [Listof `comment`s]
                                       ----------->
                                       POST: /store_comment
                                             [Listof `comment`s]

4. Add Pitch

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


5. Send Pitch

                        Dash         Flask         DB          Casper           LinkedIn


                        -------------->
                        POST: /send_pitch  
                         Pitch, user, url
                         # of messages 
                         to send  

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
                                      Pitch, user, pass, url,  
                                      [Listof userids]
                                      <----------------------------
                                       [Listof `comment`s] 
                                       --------------->
                                        [listof userids],
                                        pitch