/**************************************************
 *              IMPORT LIBRARIES                  *
 **************************************************/

var casper = require('casper').create({
<<<<<<< HEAD
    //logLevel: "debug",
    //verbose: true,
    waitTimeout: 30000,
=======
>>>>>>> 1a018486109a40cf25d90a4660945144eaf17ee4
    pageSettings: {
        loadImages:  false,        // do not load images
        loadPlugins: false         // do not load NPAPI plugins (e.g. Flash)
    }
});
var _ = require('lodash-node');
var system = require('system');


/**************************************************
 *               ERROR CALLBACKS                  *
 **************************************************/

casper.onConsoleMessage = function(msg) {
    system.stderr.writeLine('console: ' + msg);
};

casper.onError = function(msg, trace) {
    var msgStack = ['ERROR: ' + msg];
    if (trace && trace.length) {
        msgStack.push('TRACE:');
        trace.forEach(function(t) {
            msgStack.push(' -> ' + t.file + ': ' + t.line + (t.function ? ' (in function "' + t.function + '")' : ''));
        });
    }
    console.error(msgStack.join('\n'));
};


phantom.onError = function(msg, trace) {
    var msgStack = ['PHANTOM ERROR: ' + msg];
    if (trace && trace.length) {
        msgStack.push('TRACE:');
        trace.forEach(function(t) {
            msgStack.push(' -> ' + (t.file || t.sourceURL) + ': ' + t.line + (t.function ? ' (in function ' + t.function + ')' : ''));
        });
    }
    console.error(msgStack.join('\n'));
    phantom.exit(1);
};


/**************************************************
 *             GLOBAL CONSTANTS                   *
 **************************************************/

// Note: LinkedIn retrieves 6 comments/click
var LINKEDIN_LOAD_AMOUNT = 6;

/**
GLOBAL VARIABLES
**/
var comments = [];
var comments_count = 0;

var auth = {
  user: casper.cli.get('user'),
  pass: casper.cli.get('pass'),
};
var groupUrl = casper.cli.get('discuss-url');

/**************************************************
 *                  HELPERS                       *
 **************************************************/

// TODO: Use logged in session/cookies -- http://stackoverflow.com/questions/15907800/how-to-persist-cookies-between-different-casperjs-processes
var amILoggedIn = function() {
  return !(this.getTitle().indexOf('Sign In') >= 0);
} 

// TODO: Accept filename paramater
var captureScreen = function() {
  this.capture('/vagrant/test.png');
}

var captureComments = function() {
  var comments = document.querySelectorAll('li.comment-item');
  return Array.prototype.map.call(comments, function(e) {
    var comment = {}
    comment.name = e.querySelector('p.commenter').innerText;
    var names = e.querySelector('p.commenter').innerText.split(' ');
    comment['fname'] = names[0];
    comment['lname'] = names[names.length-1];
    comment['byline'] = e.querySelector('p.commenter-headline').innerText
    comment['comment'] = e.querySelector('p.comment-body').innerText;
    comment['likes'] = e.querySelector('a.like-comment').innerText.replace( /[^\d]+/g, '') || 0;
    comment['date'] = e.querySelector('li.timestamp').innerText;
    comment['userID'] = e.querySelector('a.commenter').href.split('memberID=')[1];
    var profilePartial = 'https://www.linkedin.com/profile/view?id='
    comment['profileURL'] = profilePartial + comment.userID;
    image = e.querySelector('img');
    comment['image_src'] = image.src;
    comment['connection'] = '';
    comment['isFirstDegree'] = '';

    return comment;
  });
}

var moreComments = function() {
  document.getElementById('inline-pagination').click();
}


/**************************************************
 *                    LOGIN                       *
 **************************************************/

// Login to LinkedIn
// TODO: Stay logged in via session & cookie management
casper.start('https://www.linkedin.com/uas/login', function login() {
  this.fill('form#login', {session_key: auth.user, session_password: auth.pass}, true)
});


// Skip Send Pitch
casper.thenBypassIf(function(){
    return !casper.cli.has('send-pitch');
}, 2); 


/**************************************************
 *                    SEND PITCH                  *
 **************************************************/

// Send pitch to user
<<<<<<< HEAD
// Side Effect: Will send `toUserID` a message with given pitch
casper.waitFor(amILoggedIn, function(){
=======
// Side Effect: Will send them a message with given pitch
casper.then(function(){
>>>>>>> 1a018486109a40cf25d90a4660945144eaf17ee4
  var toUserID = casper.cli.get('to-user-id');
  var pitchSubject = casper.cli.get('pitch-subject');
  var pitchBody = casper.cli.get('pitch-body').replace(/\\n/g,'\n');
  var sendPitch = !!casper.cli.get('send-pitch');
<<<<<<< HEAD
  var groupID = casper.cli.get('group-id');
=======
  var groupID = '4117360'
>>>>>>> 1a018486109a40cf25d90a4660945144eaf17ee4

  var msgPartial = 'https://www.linkedin.com/groups?viewMemberFeed=&gid='+groupID+'&memberID='
  var msgUrl = msgPartial + toUserID;

  this.thenOpen(msgUrl, function(){
    this.click('#control_gen_7');
<<<<<<< HEAD
    this.fill('form#send-msg-form', {subject: pitchSubject, body: pitchBody}, sendPitch);
    if (!sendPitch) {
        this.capture('/vagrant/message_'+toUserID+'.png');
    }
    this.echo(JSON.stringify({'sent': sendPitch, 'to': toUserID}));
=======
    this.fill('form#send-msg-form', {subject: pitchSubject, body: pitchBody}, false);
    this.capture('/vagrant/message_'+toUserId+'.png');
>>>>>>> 1a018486109a40cf25d90a4660945144eaf17ee4
  });
});

casper.then(function(){
  this.exit();
});


/**************************************************
 *         IMPORT COMMENTS FROM DISCUSSION        *
 **************************************************/

// Once logged in, open up the discussion url
casper.waitFor(amILoggedIn, function(){
<<<<<<< HEAD
  var groupUrl = casper.cli.get('discuss-url');
=======
>>>>>>> 1a018486109a40cf25d90a4660945144eaf17ee4
  this.open(groupUrl)
});

// Keep loading all comments until we reach the total
casper.then(function(){
    var total = this.evaluate(function(){ 
        return parseInt(document.querySelector('span.count').innerText) 
    });

<<<<<<< HEAD
    for (var i=0; i<(total/LINKEDIN_LOAD_AMOUNT); i++) {
        this.waitWhileSelector('#inline-pagination.loading', function() {
            this.click('#inline-pagination');
        })}
=======
  var display = '';
  for (var i=0; i<(total/LINKEDIN_LOAD_AMOUNT); i++) {
     this.waitWhileSelector('#inline-pagination.loading', function() {
         if (display != 'none') {
           this.click('#inline-pagination');
           display = this.evaluate(function(){
             return document.getElementById('inline-pagination').style.display;
           });
         }
     });
  }
>>>>>>> 1a018486109a40cf25d90a4660945144eaf17ee4
});

// Capture comments from discussion
casper.then(function(){
  comments = this.evaluate(captureComments);
  comments = _.uniq(comments, function(comment) { return comment.name; }); 
  comments_count = comments.length;
});


/**************************************************
 *    EXTRACT ADDITIONAL USER PROFILE DETAILS     *
 **************************************************/

// View their profile & retrieve connection degree info (1st, 2nd, 3rd)
// Note: -1 means out of network
// Side Effect: Will show up on their 'People Viewed Your Profile'
casper.then(function(){
  this.each(comments, function(self, comment){
    this.thenOpen(comment.profileURL, function(){
      comment['connection'] = parseInt(this.fetchText('span.fp-degree-icon')) || -1;
      comment['isFirstDegree'] = comment['connection'] == 1;
    });
  });
});

casper.run(function(){
  this.echo(JSON.stringify(comments));
  this.exit();
});
