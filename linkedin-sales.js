var casper = require('casper').create();
var _ = require('lodash-node');
var system = require('system');
phantom.page.injectJs( 'https://cdn.firebase.com/js/client/1.0.15/firebase.js');

/**
ERROR CALLBACKS
**/
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

/**
GLOBAL CONSTANTS
**/
// Note: LinkedIn retrieves 6 comments/click
var LINKEDIN_LOAD_AMOUNT = 6;

// All template fields defiend in `captureComments`
var PITCH_SUBJECT = _.template('Hello!');
var PITCH_LINES = ['Hello <%= fname %>,\n', 
                   'More content here', 
                   '\nThanks,', 
                   'Praful']
var PITCH_BODY = _.template(PITCH_LINES.join('\n'));

/**
GLOBAL VARIABLES
**/
var comments = [];
var comments_count = 0;

// TODO: Move out of this file
var auth = {
  user: "jamespsteinberg@gmail.com",
  pass: "8iN42haKAYA"
};

//var groupUrl = 'https://www.linkedin.com/groups/if-you-were-asked-try-4117360.S.5865477729327009793?view=&gid=4117360&type=member&item=5865477729327009793&report%2Esuccess=KFBepuKGen-KgW-5xqS-b-STrCfXRn9x6PnsS7U_hjTXeniek-ssQLCBwAyQhooJ6W9TPod_Yg_vRcMhHLh7GUlDhuiKMcLJCBy6bPU_i5TXeDnNgP8jvaHiY8BvRcLxTvbjbWHihXSnUxGx6-MToLHMrX6nRQneyW9Bbn0Mi09oenXYyB6wQMJkrgK3ee5YyruBdxM11tL%EF%BB%BF'
var groupUrl = 'https://www.linkedin.com/groups/I-am-working-on-trying-4117360.S.5896995984176590850?qid=6eefc472-190e-48c5-9378-854f8c171ab6&goback=%2Egde_4117360_member_5865477729327009793%2Egmp_4117360'

/**
Helper Functions
**/

// TODO: Use logged in session/cookies -- http://stackoverflow.com/questions/15907800/how-to-persist-cookies-between-different-casperjs-processes
var amILoggedIn = function() {
  return this.evaluate(function rock(){
    return document.querySelectorAll('li.nav-item').length > 3;
  });
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

var getToday = function() {
    var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth()+1; //January is 0!
        var yyyy = today.getFullYear();
        if(dd<10) {
          dd='0'+dd
        } 
        if(mm<10) {
        mm='0'+mm
        } 
        today = mm+'/'+dd+'/'+yyyy;
    return today;
}

/**
Casper Navigation
**/
// Login to LinkedIn
// TODO: Stay logged in via session & cookie management
casper.start('https://www.linkedin.com/uas/login?goback=&trk=hb_signin', function login() {
  this.echo('Logging In...');
  this.fill('form#login', {session_key: auth.user, session_password: auth.pass}, true)
});

// Once logged in, open up the discussion url
casper.waitFor(amILoggedIn, function(){
  this.echo('Open group...');
  this.open(groupUrl)
});

// Keep loading all comments until we reach the total
casper.then(function(){
  var total = this.evaluate(function(){ 
    return parseInt(document.querySelector('span.count').innerText) 
  });

  this.echo('Total: ' + total);

  var display = '';
  for (var i=0; i<(total/LINKEDIN_LOAD_AMOUNT); i++) {
     this.waitFor(
       function(){ 
          return !this.exists('#inline-pagination.loading'); 
       },
       function(){ 
         if (display != 'none') {
           this.click('#inline-pagination');
           display = this.evaluate(function(){
             return document.getElementById('inline-pagination').style.display;
           });
         }
       });
  }
});

// Capture comments from discussion
casper.then(function(){
  this.echo('Capturing comments...');
  comments = this.evaluate(captureComments);
  comments = _.uniq(comments, function(comment) { return comment.name; }); 
  comments.splice(10);
  comments_count = comments.length;
  this.echo('Comments count: ' + comments_count);
});

// View their profile & retrieve connection degree info (1st, 2nd, 3rd)
// Note: -1 means out of network
// Side Effect: Will show up on their 'People Viewed Your Profile'
casper.then(function(){
  this.each(comments, function(self, comment){
    this.thenOpen(profileURL, function(){
      comment['connection'] = parseInt(this.fetchText('span.fp-degree-icon')) || -1;
      comment['isFirstDegree'] = comment['connection'] == 1;
    });
  });
});

// Capture comments from discussion
// Side Effect: Will send them a message with given pitch
casper.then(function(){
  this.each(comments, function(self, comment){
    var msgPartial = 'https://www.linkedin.com/groups?viewMemberFeed=&gid=4117360&memberID='
    var messageToID = comment.userID;
    var msgUrl = msgPartial + messageToID
    this.echo('Message URL: ' + msgUrl);

    this.thenOpen(msgUrl, function(){
      this.click('#control_gen_7');
      this.sendKeys('#send-message-subject', PITCH_SUBJECT(comment));
      this.sendKeys('#send-message-body', PITCH_BODY(comment));
      this.then(function(){
	     // send message
         /*if (!comment.isFirstDegree){ // TODO: || inFirebase(comment.id)
            this.click('#send-message-submit');
         }*/
         this.capture('/vagrant/message_'+i+'.png');
      });
    });
  });
});

// Output comment information
casper.run(function(){
  var scoreListRef = new Firebase('https://blinding-fire-6559.firebaseio.com//userList');
  this.echo('\n'+comments_count + ' comments captured.');
  var msgPartial = 'https://www.linkedin.com/groups?viewMemberFeed=&gid=4117360&memberID='
  
  for (var i=0; i<comments_count; i++){ 
    var comment = comments[i];
    this.echo(comment.name); 
    this.echo(comment.userID); 
    this.echo(comment.degree);
    this.echo(comment.isFirstDegree);
    this.echo(comment.image_src);
    
    var messageToID = comment.userID;
    var msgUrl = msgPartial + messageToID
    var userScoreRef = scoreListRef.child(id);
    userScoreRef.set({name:comment.name, 
                      id:comment.userID, 
                      comment:comment.comment, 
                      url:msgUrl, 
                      sender:auth.user, 
                      date:getToday()}); 
  }
  this.exit();
});
