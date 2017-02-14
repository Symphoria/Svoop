var self = this;
var pageNo = 1;
var type = 'recent';
var blogData = [];

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

function changeUpvotes(blogId, operation) {
    $.ajax({
        url: 'http://127.0.0.1:8000/blog/update-upvotes/',
        type: 'PUT',
        dataType: 'json',
        data: {
            'blogid': blogId,
            'userid': self.userid,
            'operation': operation
        },
        success: function(message) {
            alert(message.message);
        }
    })
}

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
                    box.innerHTML += "<button type='button' class='btn btn-primary btn-sm upvote' disabled='disabled' id='" + JSONdata.blogData[i].id + "'>Upvote<span class='badge' id='" + JSONdata.blogData[i].id + "_upvotes'>" + JSONdata.blogData[i].upvotes + "</span></button>";
                } else {
                    box.innerHTML += "<button type='button' class='btn btn-primary btn-sm upvote' id='" + JSONdata.blogData[i].id + "'>Upvote<span class='badge' id='" + JSONdata.blogData[i].id + "_upvotes'>" + JSONdata.blogData[i].upvotes + "</span></button>";
                }

                box.innerHTML += "<button type='button' class='btn btn-default btn-sm downvote' id='" + JSONdata.blogData[i].id + "_downvote'>Downvote</button>";

                var feedWrapper = document.getElementById("feed-wrapper").appendChild(box);

                self.blogData.push(JSONdata.blogData[i].id);
            }
            for (let i = 0; i < self.blogData.length; i++) {
                blogId = self.blogData[i];
                console.log(blogId);
                document.getElementById(blogId.toString()).onclick = function() {
                    var updatedUpvotes = Number($("#" + self.blogData[i].toString() + "_upvotes").text()) + 1;
                    $("#" + self.blogData[i].toString() + "_upvotes").text(updatedUpvotes.toString());
                    changeUpvotes(self.blogData[i], 'upvote');
                    console.log('clicked button ' + self.blogData[i].toString());
                };
            }
            console.log("functions created");
        }
    })
}
console.log('done!!!!!');
