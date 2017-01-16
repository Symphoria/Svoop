import os

class Constant:
    def __init__(self):
        self.sendgrid_API_key = os.environ["sendgrid_key"]

    def email_template(self, confirmation_url):
        return """<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://use.fontawesome.com/19fb39091d.js"></script>
</head>
<body>
<div class="container">
    <div style="background: #2b6dd8 !important;  border-radius: 0px !important;">
        <h2 style="font-family: 'Raleway', sans-serif; color: white; font-size: 50px; font-weight: 500 !important; padding-top: 15px; padding-bottom: 15px; margin-top: 8px !important;"
            align="center">Thanks for Registering</h2>
    </div>
</div>
<div class="container">
    <p style="font-family: 'PT Sans', sans-serif;">We, the team at Svoop, are very happy to have another member join the
        Svoop community. We are always ready to welcome another enthusiast who wants to express himself/herself to the
        world.<br><br> Svoop is a platform that allow thinkers and believers such
        as yourself to broadcast to the world what you think, feel and believe. Really liked a movie you just watched?
        Write a review. Have a story to tell or maybe an idea? Tell the world. It is custom made just for you.<br><br>Svoop
        is like a podium
        where you express with words instead of speaking.<br><br>P.S. That last line is our motto by the way <i
                class="fa fa-smile-o" aria-hidden="true"></i><br><br>So what are you wating for? Click on the link below and lets get started.</p>
    <a align="center" href=""" + confirmation_url + """>""" + confirmation_url + """</a>
</div>
<div class="container" style="margin-top: 40px;
    font-size: 13px;
    background: gainsboro;
    width: 40%;">
    <p align="center" style="padding-top: 10px;">Sent with love by:<br>The Svoop Team, BH-5, IIIT Allahabad, Jhalwa, UP, India<br>For any queries
        contact:<br>Harshit Jain (iit2016060@iiita.ac.in)</p>
</div>
</body>
</html>
"""
