from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import UserForm, LoginForm, BlogForm
from .models import User, BlogData
from django.urls import reverse
from django.views import generic
import sendgrid
from constant import Constant

def send_mail_to_user(reciever_email, confirmation_url):
    cons = Constant()
    sendgrid_object = sendgrid.SendGridAPIClient(apikey=cons.sendgrid_API_key)
    data = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": reciever_email
                    }
                ],
                "subject": "Confirm account"
            }
        ],
        "from": {
            "email": "hj.harshit007@gmail.com",
            "name": "Svoop"
        },
        "content": [
            {
                "type": "text/html",
                "value": cons.email_template(confirmation_url)
            }
        ]
    }
    response = sendgrid_object.client.mail.send.post(request_body=data)

def get_form_data(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            if username is None:
                error_message = 'Please enter a Username'
                return render(request, 'blog/form.html', {'error_message': error_message, 'form': form}, )
            elif User.objects.filter(username=username).exists():
                error_message = 'This Username already exists'
                return render(request, 'blog/form.html', {'error_message': error_message, 'form': form}, )
            elif User.objects.filter(email=email).exists():
                error_message = 'You are a registered user'
                return render(request, 'blog/form.html', {'error_message': error_message, 'form': form}, )
            else:
                newuser = User.objects.create(username=username, password=password, email=email)
                confirmation_url = "http://127.0.0.1:8000/blog/confirm/" + str(newuser.id)
                send_mail_to_user(newuser.email, confirmation_url)
                return render(request, 'blog/thanks.html')
    else:
        form = UserForm()

    return render(request, 'blog/form.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if User.objects.filter(username=username).exists():
                if User.objects.get(username=username).password == password:
                    userid = User.objects.get(username=username).id
                    return HttpResponseRedirect(reverse('blog:myaccount', args=(userid,)))
                else:
                    error_message = 'Entered password is incorrect'
                    return render(request, 'blog/loginform.html', {'error_message': error_message, 'form': form})
            else:
                error_message = 'Username does not exist. Check your details or register.'
                return render(request, 'blog/loginform.html', {'error_message': error_message, 'form': form})
    else:
        form = LoginForm()

    return render(request, 'blog/loginform.html', {'form': form})


def my_account(request, userid):
    user = User.objects.get(pk=userid)
    try:
        all_blogs = user.blogdata_set.all()[0]
    except IndexError:
        return render(request, 'blog/myaccount.html',
                      {'message': "You have not created any blog.Click on Create Blog to create a blog", 'user': user})
    if len(user.blogdata_set.filter(published_date=None)) != 0:
        saved_blogs = user.blogdata_set.filter(published_date=None).order_by('-created_date')
        message = 'You have some unpublished blogs'
    else:
        saved_blogs = None
        message = None
    published_blogs = user.blogdata_set.exclude(published_date=None).order_by('-published_date')
    return render(request, 'blog/myaccount.html',
                  {'saved_blogs': saved_blogs, 'published_blogs': published_blogs, 'user': user, 'message': message})


def new_blog(request, userid):
    user = User.objects.get(pk=userid)
    form = BlogForm()
    return render(request, 'blog/blogform.html', {'form': form, 'user': user})


def save_blog(request, userid, blogid=0):
    form = BlogForm(request.POST)
    user = get_object_or_404(User, pk=userid)
    if form.is_valid():
        author_name = form.cleaned_data['author_name']
        title = form.cleaned_data['title']
        body = form.cleaned_data['body']
        if len(user.blogdata_set.filter(pk=blogid)) == 1:
            a_blog = get_object_or_404(BlogData, pk=blogid)
            a_blog.author = author_name
            a_blog.title = title
            a_blog.text = body
            a_blog.save()
        else:
            user.blogdata_set.create(author=author_name, title=title, text=body)
    return render(request, 'blog/saveform.html', {'user': user})


def edit_blog(request, userid, blogid):
    user = get_object_or_404(User, pk=userid)
    a_blog = get_object_or_404(BlogData, pk=blogid)
    form = BlogForm({'author_name': a_blog.author, 'title': a_blog.title, 'body': a_blog.text})
    return render(request, 'blog/editform.html', {'form': form, 'user': user, 'a_blog': a_blog})


def publish_blog(request, userid, blogid):
    user = get_object_or_404(User, pk=userid)
    a_blog = get_object_or_404(BlogData, pk=blogid)
    a_blog.publish()
    return render(request, 'blog/publish.html', {'user': user, 'a_blog': a_blog})


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'published_blog_list'

    def get_queryset(self):
        return BlogData.objects.exclude(published_date=None).order_by('-published_date')[:6]

def activate_user(userid):
    new_user = get_object_or_404(User, pk=userid)
    new_user.is_active = True
    new_user.save()
