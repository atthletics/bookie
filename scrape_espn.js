var url ='https://www.espn.com/college-football/scoreboard/_/group/80/year/2019/seasontype/2/week/1';
var page = new WebPage()
var fs = require('fs');


page.open(url, function (status) {
        just_wait();
});

function just_wait() {
    setTimeout(function() {
               fs.write('espn.html', page.content, 'w');
            phantom.exit();
    }, 10000);
}
