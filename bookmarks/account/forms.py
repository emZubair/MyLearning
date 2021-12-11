from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class EmailSendingForm(forms.Form):
    email = forms.EmailField()
