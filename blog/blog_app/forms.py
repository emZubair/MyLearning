from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    """
    A form to get Email related information from the User
    """

    name = forms.CharField(max_length=64)
    email = forms.EmailField()
    receiver_email = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
