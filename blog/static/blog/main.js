var self = this;
var pageNo = 1;
var type = 'recent';

// if (localStorage.getItem("userId") === null) {
//     var siteURL = window.location.href;
//     var userid = siteURL.split("/")[5];
//     localStorage.setItem('userId', userid);
// } else {
//     var userid = localStorage.getItem("userId");
// }

var siteURL = window.location.href;
var userid = siteURL.split("/")[5];

document.addEventListener('DOMContentLoaded', function() {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: 'http://127.0.0.1:8000/blog/user-data/?userId=' + self.userid,
        success: function(data) {
            var userName = data.user.username;
            var imageURL = data.imageURL;
            $('.username').text(userName);
            document.getElementById("Userimage").src = imageURL;
        }
    });

    getBlogData();
});

function getBlogData() {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: 'http://127.0.0.1:8000/blog/get-blogdata/?userId=' + self.userid + '&pageNo=' + self.pageNo.toString() + '&type=' + self.type,
        success: function(JSONdata) {
            for (var i = 0; i < JSONdata.blogData.length; i++) {
                var box = document.createElement("div");
                box.className = "box";
                box.innerHTML += "<h1 class='title'>" + JSONdata.blogData[i].title + "</h1>" +
                    "<hr class='divider'>" +
                    "<p class='matter'>" + JSONdata.blogData[i].text + "</p>";

                if (JSONdata.blogList.indexOf(JSONdata.blogData[i].id) > -1) {
                    box.innerHTML += "<button type='button' class='btn btn-primary btn-sm upvote' disabled='disabled'>Upvote<span class='badge'>" + JSONdata.blogData[i].upvotes + "</span></button>";
                } else {
                    box.innerHTML += "<button type='button' class='btn btn-primary btn-sm upvote'>Upvote<span class='badge'>" + JSONdata.blogData[i].upvotes + "</span></button>";
                }

                box.innerHTML += "<button type='button' class='btn btn-default btn-sm downvote'>Downvote</button>";

                var feedWrapper = document.getElementById("feed-wrapper").appendChild(box);
            }
        }
    })
}
console.log('done!!!!!');
