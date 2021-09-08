from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .forms import ImageCreateForm
from .models import Image


# Create your views here.

@login_required
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        print(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # assign current user to teh item
            new_item.user = request.user
            new_item.save()
            messages.success(request, "Image added succesfully")
            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    return render(request,
                  'images/image/create.html',
                  {'section': 'images',
                   'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request,
                  'images/image/detail.html',
                  {'section': 'images',
                   'image': image})


@login_required
@require_POST #returns HttpResponseNotAllowed object (405) if the HTTP request is not done via POST - allow only POST request for this view.
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    print(request.POST)
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            """
            Note:
            Manager provided by Django for the users_like many-to-many field of the Image model in order 
            to add or remove objects from the relationship using the add() or remove() methods. Calling add(), 
            that is, passing an object that is already present in the related object set, does not duplicate it. 
            Calling remove() and passing an object that is not in the related object set does nothing. 
            Another useful method of many-to-many managers is clear(), which removes all objects from the related object set.   
                    
            """

            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})

