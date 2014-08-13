/**************************************************
 *              IMPORT LIBRARIES                  *
 **************************************************/

var DEBUG = false; 

var casper = require('casper').create({
    logLevel: DEBUG? "debug" : "error",
    verbose: DEBUG,
    waitTimeout: 30000,
    pageSettings: {
        loadImages:  false,        // do not load images
        loadPlugins: false,         // do not load NPAPI plugins (e.g. Flash)
    }
});
var _ = require('lodash-node');
var system = require('system');
var fs = require('fs');


/**************************************************
 *               ERROR CALLBACKS                  *
 **************************************************/

// Check for errors in all pages received from LinkedIn
casper.on('resource.received', function(resource) {
    var errors  = casper.evaluate(function(){
        var errs = []; 
        var getErrors = document.querySelectorAll('.error');

        for (var i=0; i<getErrors.length; i++) { 
            error = getErrors[i].innerText.trim();
            
            // Ignore undisplayed errors on page or error is empty string
            if (!getErrors[i].offsetParent || !error){
                continue;
            }
            errs.push(error);
        }
        return errs;
    });

    if (errors.length) {
        casper.die(JSON.stringify({'errors': errors, 'data': casper.cli.options}));
    }
});

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
var BASE_DIR = '/vagrant'

/**
GLOBAL VARIABLES
**/
var comments = [];
var comments_count = 0;

var auth = {
  user: casper.cli.get('user'),
  pass: casper.cli.get('pass'),
  name: casper.cli.get('first-name'),
};


/**************************************************
 *                  HELPERS                       *
 **************************************************/

var check_login = 1;
var amILoggedIn = function() {
    DEBUG && casper.capture(BASE_DIR + '/logging-in'+check_login+'.png');
    check_login += 1;
    var logged_in = casper.evaluate(function(){
        return document.querySelectorAll('.nav-item').length > 3;
    });
    return logged_in;
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

// Load up our cookies
/*
var file = auth.name+"-cookies.txt";
if (fs.exists(file)) {
    var data = fs.read(file)
    phantom.cookies = JSON.parse(data)
}
*/

// Skip login if our cookies are good
casper.start('https://www.linkedin.com/', function() {
    //console.log(data);
    DEBUG && this.capture(BASE_DIR + '/linkedin.png');
});

// Test if we're already logged in
casper.thenBypassIf(amILoggedIn, 2);

// Login if cookies are expired or missing
// thenOpen counts as 2 steps
casper.thenOpen('https://www.linkedin.com/uas/login', function(){
        this.fill('form#login', {session_key: auth.user, session_password: auth.pass}, true)
        DEBUG && this.capture(BASE_DIR + '/login.png');
});


// Send Pitch and Import Discussion are two separate steps
// We only check for Send Pitch, we'll need more checks as we add steps
casper.thenBypassIf(function(){
    return !casper.cli.has('send-pitch');
}, 2); 


/**************************************************
 *                    SEND PITCH                  *
 **************************************************/

// Send pitch to user
// Side Effect: Will send `toUserID` a message with given pitch
casper.waitFor(amILoggedIn, function(){
  var toUserID = casper.cli.get('to-user-id');
  var pitchSubject = casper.cli.get('pitch-subject');
  var pitchBody = casper.cli.get('pitch-body').replace(/\\n/g,'\n');
  var sendPitch = false; //!!casper.cli.get('send-pitch');
  var groupID = casper.cli.get('group-id');

  var msgPartial = 'https://www.linkedin.com/groups?viewMemberFeed=&gid='+groupID+'&memberID='
  var msgUrl = msgPartial + toUserID;

  this.thenOpen(msgUrl, function(){
    this.click('#control_gen_7');
    this.fill('form#send-msg-form', {subject: pitchSubject, body: pitchBody}, sendPitch);
    DEBUG && this.capture(BASE_DIR + '/message_'+toUserID+'.png');
    this.echo(JSON.stringify({'sent': sendPitch, 'to': toUserID}));
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
    DEBUG && this.capture(BASE_DIR + '/homepage.png');
    var groupUrl = casper.cli.get('discuss-url');
    this.open(groupUrl)
});

// Keep loading all comments until we reach the total
casper.then(function(){
    DEBUG && this.capture(BASE_DIR + '/group.png');
    var total = this.evaluate(function(){ 
        return parseInt(document.querySelector('span.count').innerText) 
    });

    // if there's no pagination button, quit
    if (!this.exists('#inline-pagination')) {
       return;
    }

    for (var i=0; i<(total/LINKEDIN_LOAD_AMOUNT); i++) {
        this.waitWhileSelector('#inline-pagination.loading', function() {
            this.click('#inline-pagination');
        })}
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
            DEBUG && this.capture(BASE_DIR + '/profile'+comment['userID']+'.png');
            comment['connection'] = parseInt(this.fetchText('span.fp-degree-icon')) || -1;
            comment['isFirstDegree'] = comment['connection'] == 1;
        });
    });
});

casper.run(function(){ 
  this.echo(JSON.stringify(comments));
  this.exit();
});
