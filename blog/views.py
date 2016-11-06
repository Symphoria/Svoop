from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserForm
from .models import User


def get_form_data(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            if User.objects.filter(username=username).exists():
                error_message = 'This Username already exists'
                return render(request, 'blog/form.html', {'error_message': error_message, 'form': form}, )
            elif User.objects.filter(email=email).exists():
                error_message = 'You are a registered user'
                return render(request, 'blog/form.html', {'error_message': error_message, 'form': form}, )
            else:
                User.objects.create(username=username, password=password, email=email)
                return render(request, 'blog/thanks.html')
    else:
        form = UserForm()

    return render(request, 'blog/form.html', {'form': form})
