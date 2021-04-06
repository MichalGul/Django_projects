from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def user_login(request): # Custom login view
    if request.method == 'POST': # if form is submited
        print(request.POST)
        form = LoginForm(request.POST) # Instantiate the form with the submitted data with form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['name'],
                                password=cd['password']) # check user credentials and returns a User object if corected
            if user is not None:
                if user.is_active:
                    login(request, user) #just like flask, sets user in the current session
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else: #render form when get request
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})
