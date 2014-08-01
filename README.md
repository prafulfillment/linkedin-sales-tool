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