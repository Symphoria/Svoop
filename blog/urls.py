from django.conf.urls import url
import views

app_name = 'blog'
urlpatterns = [
    url(r'^register/$', views.get_form_data, name='register')
]
