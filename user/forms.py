from django import forms
from django.contrib import auth
from .models import Profile
from django.core.validators import ValidationError



class LoginForm(forms.Form):
    id = forms.CharField(label="ID", max_length=20)
    password = forms.CharField(label="PASSWORD", max_length=20, widget=forms.PasswordInput)

class JoinForm(forms.Form):
    id = forms.CharField(label="ID", max_length=20)
    password = forms.CharField(label="PASSWORD", min_length=4, max_length=20, widget=forms.PasswordInput)
    password_check = forms.CharField(
        label="PASSWORD(again)", min_length=4, max_length=20, widget=forms.PasswordInput)
    email_address = forms.EmailField(label="Email Address")

    def clean(self):
        # get_user_model helper 함수를 통해 모델 클래스 참조
        User = auth.get_user_model()
        
        cleaned_data = super().clean()
        
        # 패스워드 동일 체크
        if cleaned_data.get("password")!= cleaned_data.get("password_check"):
            raise ValidationError('비밀번호를 동일하게 입력해주십시오.')
        
        # ID 중복여부
        if User.objects.filter(username=cleaned_data.get(("username"))).exists():
            raise ValidationError('아이디가 이미 사용중입니다.')
    
        return cleaned_data
        
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)

        super(JoinForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.initial['id'] = self.instance.username
            self.initial['email_address'] = self.instance.email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number',)