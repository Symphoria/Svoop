var self = this;
var pageNo = 1;
var siteURL = window.location.href;
var userid = siteURL.split("/").reverse()[1];

document.addEventListener('DOMContentLoaded', function() {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: 'http://127.0.0.1:8000/blog/user-data/?userId=' + self.userid,
        success: function(data) {
            var userName = data.user.username;
            var imageURL = data.imageURL;
            $('#username .username').text(userName);
            document.getElementById("Userimage").src = imageURL;
        }
    })
});
