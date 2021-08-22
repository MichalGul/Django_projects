from django import forms
from .models import Image

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