from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

app_name = 'blog'
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="blog/home.html"), name="home"),
    url(r'^login/(?P<userid>[0-9]+)/$', views.index_view, name='index'),
    url(r'^register/$', views.get_form_data, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^confirm/(?P<userid>[0-9]+)/$', views.activate_user, name='confirm_user'),
    url(r'^login/(?P<userid>[0-9]+)/account/$', views.my_account, name='myaccount'),
    url(r'^thanks/$', TemplateView.as_view(template_name="blog/thanks.html"), name='thanks'),
    url(r'^logging-out/$', views.user_logout, name='logout'),
    url(r'^login/(?P<userid>[0-9]+)/set_image/$', views.set_user_image, name='set_image'),
    url(r'^update-upvotes/', views.UpdateUpvotes.as_view()),
    url(r'^get-blogdata/', views.AllBlogView.as_view()),
    url(r'^user-data/', views.UserDataView.as_view())
]
