from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ImageForm


@login_required
def create_image(request):
    if request.method == 'POST':
        image_form = ImageForm(data=request.POST)
        if image_form.is_valid():
            cd = image_form.cleaned_data
            new_item = image_form.save(commit=False)
            new_item.user = request.user

            new_item.save()
            messages.success(request, "Image saved successfully")
            return redirect(new_item.get_absolute_url())
    else:
        image_form = ImageForm(data=request.GET)

    return render(request, 'bookmarks/images/create.html', {
        'section': 'images', 'form': image_form
    })

