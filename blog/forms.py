from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=200)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    email = forms.EmailField()


class BlogForm(forms.Form):
    author_name = forms.CharField(label='Author Name', max_length=100)
    title = forms.CharField(label='Title', max_length=150)
    body = forms.CharField(label='Body', widget=forms.Textarea)


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=200)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    keep_logged_in = forms.CharField(label='keep_logged_in')


class PhotoForm(forms.Form):
    image = forms.ImageField(label='image')
