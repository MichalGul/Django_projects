from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):  # Dynamicly create form from model
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')  # which fields fo model are user for form
