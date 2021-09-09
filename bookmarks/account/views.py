from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.http import require_POST

from actions.models import Action
from actions.utils import create_action
from common.decorators import ajax_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Contact
from .models import Profile


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
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    print(request.user.following)
    following_ids = request.user.following.values_list('id',
                                                       flat=True)
    if following_ids:
        # if user is following others, retrive only their actions
        actions = actions.filter(user_id__in=following_ids)
    actions = actions[:10]
    #actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10] #  use user__profile to join the Profile table in a single SQL query
    print([action.verb for action in actions])
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard',
                   'actions': actions})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password( # hash user password
                user_form.cleaned_data['password']
            )
            # Save user object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account')
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    print(request.method)
    if request.method == 'POST':
        print(request.user)
        print(request.POST)
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                  'account/user/list.html',
                  {'section': 'people',
                   'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request,
                  'account/user/detail.html',
                  {'section': 'people',
                   'user': user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                """
                Since you are using a custom intermediary model for the user's many-to-many relationship, 
                the default add() and remove() methods of the automatic manager of ManyToManyField are not available. 
                You use the intermediary Contact model to create or delete user relationships. 
                """
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
                create_action(request.user, 'is following', user)
            else:
                # unfollow
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()

            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status': 'error'})
