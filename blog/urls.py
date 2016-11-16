from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^register/$', views.get_form_data, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^login/(?P<userid>[0-9]+)/$', views.my_account, name='myaccount'),
    url(r'^login/(?P<userid>[0-9]+)/new-blog/$', views.new_blog, name='new-blog'),
    url(r'^login/(?P<userid>[0-9]+)/save-blog/$', views.save_blog, name='save-blog'),
    url(r'^login/(?P<userid>[0-9]+)/(?P<blogid>[0-9]+)/$', views.save_blog, name='saved-blogs'),
    url(r'^login/(?P<userid>[0-9]+)/(?P<blogid>[0-9]+)/edit/$', views.edit_blog, name='edit-blog'),
    url(r'^login/(?P<userid>[0-9]+)/(?P<blogid>[0-9]+)/blog-published/$', views.publish_blog, name='publish-blog')
]
