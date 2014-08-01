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
var comments = [];
var comments_count = 0;

var auth = {
  user: "jamespsteinberg@gmail.com",
  pass: "8iN42haKAYA"
};

var groupUrl = 'https://www.linkedin.com/groups/if-you-were-asked-try-4117360.S.5865477729327009793?view=&gid=4117360&type=member&item=5865477729327009793&report%2Esuccess=KFBepuKGen-KgW-5xqS-b-STrCfXRn9x6PnsS7U_hjTXeniek-ssQLCBwAyQhooJ6W9TPod_Yg_vRcMhHLh7GUlDhuiKMcLJCBy6bPU_i5TXeDnNgP8jvaHiY8BvRcLxTvbjbWHihXSnUxGx6-MToLHMrX6nRQneyW9Bbn0Mi09oenXYyB6wQMJkrgK3ee5YyruBdxM11tL%EF%BB%BF'
//var groupUrl = 'https://www.linkedin.com/groups/I-am-working-on-trying-4117360.S.5896995984176590850?qid=6eefc472-190e-48c5-9378-854f8c171ab6&goback=%2Egde_4117360_member_5865477729327009793%2Egmp_4117360'

/**
Helper Functions
**/

var amILoggedIn = function() {
  return this.evaluate(function rock(){
    return document.querySelectorAll('li.nav-item').length > 3;
  });
} 

var captureScreen = function() {
  this.capture('/vagrant/test.png');
}

var captureComments = function() {
  var comments = document.querySelectorAll('li.comment-item');
  return Array.prototype.map.call(comments, function(e) {
    var comment = {}
    comment.name = e.querySelector('p.commenter').innerText;
    names = e.querySelector('p.commenter').innerText.split(' ');
    comment.fname = names[0];
    comment.lname = names[names.length-1];
    comment.byline = e.querySelector('p.commenter-headline').innerText
    comment.comment = e.querySelector('p.comment-body').innerText;
    comment.likes = e.querySelector('a.like-comment').innerText.replace( /[^\d]+/g, '') || 0;
    comment.date = e.querySelector('li.timestamp').innerText;
    comment.userID = e.querySelector('a.commenter').href.split('memberID=')[1];
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
  var i = 0;
  var total = this.evaluate(function(){ 
    return parseInt(document.querySelector('span.count').innerText) 
  });

  console.log('Total: ' + total);
  var display = '';

  for (var i=0; i<(total/20); i++) {
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
  //comments.splice(0, 10);
  comments.splice(10);
  comments_count = comments.length;
  this.echo('Comments count: ' + comments_count);
});

var i = 0;
// Capture comments from discussion
// Side Effect: Will send them a message with given pitch
casper.then(function(){
  this.each(comments, function(self, comment){
    var msgPartial = 'https://www.linkedin.com/groups?viewMemberFeed=&gid=4117360&memberID='
    var messageToID = comment.userID;
    var msgUrl = msgPartial + messageToID
    console.log('Message URL: ' + msgUrl);

    this.thenOpen(msgUrl, function(){
      this.click('#control_gen_7');
      this.sendKeys('#send-message-subject', 'Hello!');
      var body = _.template('Hi <%= fname %>, \n \n My name is James and I\'m a co-founder at derivative/d. We help warehouses automate their pallet movement for a low monthly cost. Think Kiva Systems, but on a rental model. \n \n I saw you posted in the thread on optimizing 10% of a warehouse and wanted to learn more about how you currently handle your operations. \n \n Are you available for a quick call later next week? \n \n Cheers, \n James \n derivative/d');
      this.sendKeys('#send-message-body', body(comment));
      this.then(function(){
	// send message
        //this.click('#send-message-submit');
        this.capture('/vagrant/message_'+i+'.png');
        i+=1;
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
    this.echo(comments[i].name); 
    this.echo(comments[i].userID); 
    
    var messageToID = comment.userID;
    var msgUrl = msgPartial + messageToID
    var userScoreRef = scoreListRef.child(id);
    userScoreRef.set({name:comments[i].name, id:comments[i].userID, comment:comments[i].comment, url:msgUrl, sender:"James", date:getToday()}); 
  }
  this.exit();
});
