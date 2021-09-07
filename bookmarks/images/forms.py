from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput, # This widget is rendered as an HTML input element with a type="hidden" attribute
        }

    # This method is executed for each field when call is_valid()
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['.jpg', '.jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extension')
        return url

    # override ModelForm save method to download image from given url (commit responsible for putting date to database)
    def save(self, force_insert=False, force_update=False, commit=True):
        # create a new image empty (model) instance
        image = super().save(commit=False)
        # get url data from form
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'
        # download image from the given URL and call save of image  method of the image field,
        # passing it a ContentFile object that is instantiated with the downloaded file content.
        # In this way, you save the file to the media directory of your project.
        # You pass the save=False parameter to avoid saving the object to the database yet
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()),
                         save=False)
        if commit: # save to database only when commit is set to true
            image.save()
        return image