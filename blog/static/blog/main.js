var self = this;
var globalObject = {
    pageNo: 1,
    type: 'recent',
    blogData: [],
    userid: window.location.href.split("/")[5]
};

if (window.location.href.split('/').reverse()[1] == 'account') {
    globalObject.location = 'account'
} else {
    globalObject.location = 'feed'
}

document.addEventListener('DOMContentLoaded', function() {
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: 'http://127.0.0.1:8000/svoop/user-data/?userId=' + self.globalObject.userid,
        success: function(data) {
            var userName = data.user.username,
                imageURL = data.imageURL;
            $('.username').text(userName);
            $('#Userimage').attr('src', imageURL);
            $('#Userimagebig').attr('src', imageURL);
            $('#left-wrapper-username').text(userName);
        }
    });

    getBlogData();
});

function changeUpvotes(blogId, operation) {
    $.ajax({
        url: 'http://127.0.0.1:8000/svoop/update-upvotes/',
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
        url: 'http://127.0.0.1:8000/svoop/get-blogdata/?userId=' + self.globalObject.userid + '&pageNo=' + self.globalObject.pageNo.toString() + '&type=' + self.globalObject.type + '&location=' + self.globalObject.location,
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

                $(box).hide().appendTo('#feed-wrapper').fadeIn(400);

                self.globalObject.blogData.push(JSONdata.blogData[i].id);
            }

            for (let i = 0; i < self.globalObject.blogData.length; i++) {
                document.getElementById(self.globalObject.blogData[i].toString()).onclick = function() {
                    if ($('#' + self.globalObject.blogData[i].toString()).hasClass('clicked')) {
                        var updatedUpvotes = Number($("#" + self.globalObject.blogData[i].toString() + "_upvotes").text()) - 1;
                        $("#" + self.globalObject.blogData[i].toString() + "_upvotes").text(updatedUpvotes.toString());
                        $(this).removeClass('clicked');
                        $(this).html('Upvote' + "<span class='badge' id='" + self.globalObject.blogData[i].toString() + "_upvotes'>" + updatedUpvotes.toString() + "</span>");
                        changeUpvotes(self.globalObject.blogData[i], 'downvote');
                    } else {
                        var updatedUpvotes = Number($("#" + self.globalObject.blogData[i].toString() + "_upvotes").text()) + 1;
                        $("#" + self.globalObject.blogData[i].toString() + "_upvotes").text(updatedUpvotes.toString());
                        $(this).addClass('clicked');
                        $(this).html('Upvoted' + "<span class='badge' id='" + self.globalObject.blogData[i].toString() + "_upvotes'>" + updatedUpvotes.toString() + "</span>");
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
});

$('#trending a').click(function() {
    $('#recent').removeClass('active');
    $('#trending').addClass('active');
    self.globalObject.type = 'trending';
    getBlogData();
});

// I know this function is shit. But I am just feeling so lazy to do it any other efficient way :(
function validateForm() {
    var flag1 = 0,
        flag2 = 0;
    if ($('#currentPassword').val().length === 0) {
        flag1 = 1;
        $('#currentPassword').css('border-color', '#e62222');
    } else {
        $('#currentPassword').css('border-color', '');
    }
    if ($('#newPassword').val().length === 0) {
        flag1 = 1;
        $('#newPassword').css('border-color', '#e62222');
    } else {
        $('#newPassword').css('border-color', '');
    }
    if ($('#confirmPassword').val().length === 0) {
        flag1 = 1;
        $('#confirmPassword').css('border-color', '#e62222');
    } else {
        $('#confirmPassword').css('border-color', '');
    }
    if ($('#newPassword').val() !== $('#confirmPassword').val()) {
        flag2 = 1;
        $('#confirmPassword').css('border-color', '#e62222');
    } else {
        $('#confirmPassword').css('border-color', '');
    }
    if (flag1) {
        $('#changePasswordError').html("<span class='glyphicon glyphicon-remove-sign' aria-hidden='true'></span> Some Fields are Empty");
        return false;
    } else if (flag2) {
        $('#changePasswordError').html("<span class='glyphicon glyphicon-remove-sign' aria-hidden='true'></span> Passwords Do Not Match");
        return false;
    } else {
        return true;
    }
}

$('#changePasswordSubmit').click(function() {
    if (validateForm()) {
        var $btn = $(this).button('loading');

        $.ajax({
            type: 'PUT',
            dataType: 'json',
            url: 'http://127.0.0.1:8000/svoop/user-data/',
            data: {
                'userId': self.globalObject.userid
            },
            headers: {
                'currentPassword': $('#currentPassword').val(),
                'newPassword': $('#newPassword').val()
            },
            success: function(message) {
                $btn.button('reset');
                $('#changePasswordModal').modal('hide');
                $('#currentPassword').val('');
                $('#newPassword').val('');
                $('#confirmPassword').val('');
                console.log(message);
            },
            error: function(message) {
                $btn.button('reset');
                $('#changePasswordError').html("<span class='glyphicon glyphicon-remove-sign' aria-hidden='true'></span> Current Password Does Not Match");
                console.log(message);
            }
        })
    }
});

$(document).on('click', '.browse', function() {
    var file = $(this).parent().parent().parent().find('.file');
    file.trigger('click');
});
$(document).on('change', '.file', function() {
    $(this).parent().find('.form-control').val($(this).val().replace(/C:\\fakepath\\/i, ''));
});

console.log('done!!!!!');
