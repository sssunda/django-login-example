from django import forms

class LoginForm(forms.Form):
    id = forms.CharField(label="ID", max_length=20)
    password = forms.CharField(label="PASSWORD", max_length=20, widget=forms.PasswordInput)

class JoinForm(forms.Form):
    id = forms.CharField(label="ID", max_length=20)
    password = forms.CharField(label="PASSWORD", min_length=6, max_length=20, widget=forms.PasswordInput)
    password_check = forms.CharField(
        label="PASSWORD(again)", min_length=6, max_length=20, required=True, widget=forms.PasswordInput)