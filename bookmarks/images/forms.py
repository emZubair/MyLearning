from urllib import request
from django import forms
from django.utils.text import slugify
from django.core.files.base import ContentFile

from .models import Image


def get_extension_from_url(url):
    return url.split('.', 1)[1].lower()


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widget = {
            'url': forms.HiddenInput
        }

    def clean_url(self):
        url = self.cleaned_data.get('url')
        valid_extension = 'jpg jpeg png'
        extension = get_extension_from_url(url)
        if extension not in valid_extension:
            raise forms.ValidationError(f"Image URL doesn't contain valid extension:{valid_extension}")
        return url

    def save(self, commit=True):
        image = super().save(commit=False)
        url = self.cleaned_data.get('url')
        image_extension = get_extension_from_url(url)
        image_name = slugify(image.title)
        image_name_with_extension = f'{image_name}.{image_extension}'

        # Download the image from given URL
        response = request.urlopen(url)
        image.image.save(image_name_with_extension,
                         ContentFile(response.read()), save=False)
        if commit:
            image.save()
        return image
