from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import UserForm, LoginForm, BlogForm
from .models import User, BlogData
from django.urls import reverse
import sendgrid
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from constant import Constant
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import BlogSerializer, UserSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

cloudinary.config(
    cloud_name=os.environ["my_cloud_name"],
    api_key=os.environ["my_api_key"],
    api_secret=os.environ["my_api_secret"]
)


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
                confirmation_url = "http://svoop.herokuapp.com/blog/confirm/" + str(newuser.id)
                send_mail_to_user(newuser.email, confirmation_url)
                return HttpResponseRedirect(reverse('blog:thanks'))
    else:
        form = UserForm()

    return render(request, 'blog/form.html', {'form': form})


def user_login(request):
    if 'is_logged_in' not in request.session or request.session['is_logged_in'] == False:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                keep_logged_in = form.cleaned_data['keep_logged_in']
                if User.objects.filter(username=username, is_active=True).exists():
                    if User.objects.get(username=username).password == password:
                        userid = User.objects.get(username=username).id
                        request.session['user_id'] = userid
                        request.session['is_logged_in'] = True
                        if keep_logged_in == 'off':
                            request.session.set_expiry(0)
                        else:
                            request.session.set_expiry(1300000)
                        return HttpResponseRedirect(reverse('blog:index', args=(userid,)))
                    else:
                        error_message = 'Incorrect Credentials'
                        return render(request, 'blog/loginform.html', {'error_message': error_message, 'form': form})
                else:
                    error_message = 'Username does not exist. Check your details or register.'
                    return render(request, 'blog/loginform.html', {'error_message': error_message, 'form': form})
        else:
            form = LoginForm()

        return render(request, 'blog/loginform.html', {'form': form})
    else:
        if request.session['is_logged_in'] is True:
            userid = request.session['user_id']
            return HttpResponseRedirect(reverse('blog:myaccount', args=(userid,)))
        else:
            form = LoginForm()
            return render(request, 'blog/loginform.html', {'form': form})


def user_logout(request):
    request.session['is_logged_in'] = False
    return HttpResponseRedirect(reverse('blog:home'))


def my_account(request, userid):
    user = get_object_or_404(User, pk=userid)
    if 'is_logged_in' not in request.session or request.session['is_logged_in'] == False:
        return HttpResponseRedirect(reverse('blog:login'))
    else:
        try:
            all_blogs = user.blogdata_set.all()[0]
        except IndexError:
            return render(request, 'blog/myaccount.html',
                          {'message': "You have not created any blog.Click on Create Blog to create a blog",
                           'user': user})
        if len(user.blogdata_set.filter(published_date=None)) != 0:
            saved_blogs = user.blogdata_set.filter(published_date=None).order_by('-created_date')
            message = 'You have some unpublished blogs'
        else:
            saved_blogs = None
            message = None
        if user.image is not None:
            image_url = cloudinary.CloudinaryImage(user.image).build_url(width=200, height=200, crop='thumb',
                                                                         gravity='face')
        else:
            image_url = None
        published_blogs = user.blogdata_set.exclude(published_date=None).order_by('-published_date')
        return render(request, 'blog/myaccount.html',
                      {'saved_blogs': saved_blogs, 'published_blogs': published_blogs, 'user': user, 'message': message,
                       'image_url': image_url})


def index_view(request, userid):
    if 'is_logged_in' not in request.session or request.session['is_logged_in'] == False or str(
            request.session['user_id']) != userid:
        return HttpResponseRedirect(reverse('blog:login'))
    else:
        return render(request, 'blog/index.html')


def activate_user(request, userid):
    new_user = get_object_or_404(User, pk=userid)
    new_user.is_active = True
    new_user.save()
    return HttpResponseRedirect(reverse('blog:myaccount', args=(userid,)))


def set_user_image(request, userid):
    user = get_object_or_404(User, pk=userid)
    image = request.FILES['image']
    if user.image is not None:
        cloudinary.uploader.destroy(user.image)
    image_obj = cloudinary.uploader.upload(image,
                                           eager={'width': 200, 'height': 200, 'crop': 'thumb', 'gravity': 'face'})
    user.image = image_obj['public_id']
    user.save()
    return HttpResponseRedirect(reverse('blog:myaccount', args=(userid,)))


class UpdateUpvotes(APIView):
    def put(self, request):
        blog_id = request.data['blogid']
        user_id = request.data['userid']
        operation = request.data['operation']

        blog_obj = BlogData.objects.filter(pk=blog_id).first()
        user = User.objects.filter(pk=user_id).first()

        if blog_obj and user:
            if operation == 'upvote':
                blog_obj.upvotes += 1
                user.upvoted_blogs.add(blog_obj)
            else:
                blog_obj.upvotes -= 1
                if user.upvoted_blogs.filter(pk=blog_id).first():
                    user.upvoted_blogs.remove(blog_obj)
            blog_obj.save()

            return Response({'message': 'Upvotes updated'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'There was some error...'}, status=status.HTTP_404_NOT_FOUND)


class UserDataView(APIView):
    def get(self, request):
        user_id = request.GET.get('userId')
        user = User.objects.filter(pk=user_id).first()

        if user:
            if user.image is None:
                image_url = "http://res.cloudinary.com/doppel/image/upload/c_thumb,g_face,h_200,r_max,w_200/v1481639812/home-user-icon_je9kjh.png"
            else:
                image_url = cloudinary.CloudinaryImage(user.image).build_url(width=200, height=200, crop='thumb',
                                                                             gravity='face')

            payload = UserSerializer(instance=user).data

            json = {
                'user': payload,
                'imageURL': image_url
            }

            return Response(json, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        user_id = request.data['userId']
        current_password = request.META['HTTP_CURRENTPASSWORD']
        new_password = request.META['HTTP_NEWPASSWORD']

        user = get_object_or_404(User, pk=user_id)

        if user.password == current_password:
            user.password = new_password
            user.save()
            return Response({'message': 'Password Changed'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Current Password Does Not Match'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class AllBlogView(APIView):
    def get(self, request):
        user_id = request.GET['userId']
        page_no = int(request.GET['pageNo'])
        type = request.GET['type']
        location = request.GET['location']

        user = get_object_or_404(User, pk=user_id)
        blog_id_list = [blog.id for blog in user.blogdata_set.all()]
        upvoted_blog_list = [blog.id for blog in user.upvoted_blogs.all()]

        if location == 'feed':
            if type == 'recent':
                blog_queryset = BlogData.objects.exclude(id__in=blog_id_list).exclude(published_date=None).order_by(
                    '-published_date')
            else:
                blog_queryset = BlogData.objects.exclude(id__in=blog_id_list).exclude(published_date=None).order_by(
                    '-upvotes')
        else:
            blog_queryset = user.blogdata_set.exclude(published_date=None).order_by('-published_date')

        paginator = Paginator(blog_queryset, 10)
        try:
            paged_blogs = paginator.page(page_no)
        except PageNotAnInteger:
            paged_blogs = paginator.page(1)
        except EmptyPage:
            paged_blogs = paginator.page(paginator.num_pages)
        previous_exists = paged_blogs.has_previous()
        next_exists = paged_blogs.has_next()

        payload = BlogSerializer(instance=paged_blogs, many=True).data

        json = {
            'blogData': payload,
            'blogList': upvoted_blog_list,
            'hasPrevious': previous_exists,
            'hasNext': next_exists
        }

        return Response(json, status=status.HTTP_200_OK)

    def post(self, request):
        user_id = request.data['userId']
        author = request.data['author']
        title = request.data['title']
        body = request.data['mainBody']

        user = User.objects.filter(pk=user_id).first()

        if user:
            a_post = user.blogdata_set.create(author=author, title=title, text=body)
            a_post.publish()
            return Response({'message': 'Entry Created'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Some Error Occurred'}, status=status.HTTP_404_NOT_FOUND)
