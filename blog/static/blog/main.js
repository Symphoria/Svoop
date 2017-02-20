var self = this;
var globalObject = {
    pageNo: 1,
    type: 'recent',
    blogData: [],
    userid: window.location.href.split("/")[5]
};

document.addEventListener('DOMContentLoaded', function() {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: 'http://127.0.0.1:8000/blog/user-data/?userId=' + self.globalObject.userid,
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
            'userid': self.globalObject.userid,
            'operation': operation
        },
        success: function(message) {
            console.log(message.message);
        }
    })
}

function getBlogData() {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: 'http://127.0.0.1:8000/blog/get-blogdata/?userId=' + self.globalObject.userid + '&pageNo=' + self.globalObject.pageNo.toString() + '&type=' + self.globalObject.type,
        success: function(JSONdata) {
            self.globalObject.blogData = [];
            $('#feed-wrapper').empty();

            for (var i = 0; i < JSONdata.blogData.length; i++) {
                var box = document.createElement("div");
                box.className = "box";
                box.innerHTML += "<h1 class='title'>" + JSONdata.blogData[i].title + "</h1>" +
                    "<hr class='divider'>" +
                    "<p class='matter'>" + JSONdata.blogData[i].text + "</p>";

                if (JSONdata.blogList.indexOf(JSONdata.blogData[i].id) > -1) {
                    box.innerHTML += "<button type='button' class='btn btn-primary btn-sm upvote clicked' id='" + JSONdata.blogData[i].id + "'>Upvoted<span class='badge' id='" + JSONdata.blogData[i].id + "_upvotes'>" + JSONdata.blogData[i].upvotes + "</span></button>";
                } else {
                    box.innerHTML += "<button type='button' class='btn btn-primary btn-sm upvote' id='" + JSONdata.blogData[i].id + "'>Upvote<span class='badge' id='" + JSONdata.blogData[i].id + "_upvotes'>" + JSONdata.blogData[i].upvotes + "</span></button>";
                }

                document.getElementById("feed-wrapper").appendChild(box);

                self.globalObject.blogData.push(JSONdata.blogData[i].id);
            }

            for (let i = 0; i < self.globalObject.blogData.length; i++) {
                document.getElementById(self.globalObject.blogData[i].toString()).onclick = function() {
                    if ($('#' + self.globalObject.blogData[i].toString()).hasClass('clicked')) {
                        var updatedUpvotes = Number($("#" + self.globalObject.blogData[i].toString() + "_upvotes").text()) - 1;
                        $("#" + self.globalObject.blogData[i].toString() + "_upvotes").text(updatedUpvotes.toString());
                        $("#" + self.globalObject.blogData[i].toString()).removeClass('clicked');
                        $("#" + self.globalObject.blogData[i].toString()).html('Upvote' + "<span class='badge' id='" + self.globalObject.blogData[i].toString() + "_upvotes'>" + updatedUpvotes.toString() + "</span>");
                        changeUpvotes(self.globalObject.blogData[i], 'downvote');
                    } else {
                        var updatedUpvotes = Number($("#" + self.globalObject.blogData[i].toString() + "_upvotes").text()) + 1;
                        $("#" + self.globalObject.blogData[i].toString() + "_upvotes").text(updatedUpvotes.toString());
                        $("#" + self.globalObject.blogData[i].toString()).addClass('clicked');
                        $("#" + self.globalObject.blogData[i].toString()).html('Upvoted' + "<span class='badge' id='" + self.globalObject.blogData[i].toString() + "_upvotes'>" + updatedUpvotes.toString() + "</span>");
                        changeUpvotes(self.globalObject.blogData[i], 'upvote');
                    }

                    console.log('clicked button ' + self.globalObject.blogData[i].toString());
                };
            }

            if (JSONdata.hasPrevious) {
                $('#previous').removeClass('disabled');
            } else {
                $('#previous').addClass('disabled');
            }

            if (JSONdata.hasNext) {
                $('#next').removeClass('disabled');
            } else {
                $('#next').addClass('disabled');
            }
        }
    })
}

$('li#next a').click(function() {
    self.globalObject.pageNo += 1;
    getBlogData();
});

$('li#previous a').click(function() {
    self.globalObject.pageNo -= 1;
    getBlogData();
});

$('#recent a').click(function() {
    $('#trending').removeClass('active');
    $('#recent').addClass('active');
    self.globalObject.type = 'recent';
    getBlogData();
})

$('#trending a').click(function() {
    $('#recent').removeClass('active');
    $('#trending').addClass('active');
    self.globalObject.type = 'trending';
    getBlogData();
})

console.log('done!!!!!');
