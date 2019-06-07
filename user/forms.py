from django import forms
from django.contrib import auth
from .models import Profile
from django.core.validators import ValidationError, EmailValidator

class LoginForm(forms.Form):
    id = forms.CharField(label='', max_length=20)
    password = forms.CharField(label='', max_length=20, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({'placeholder': ' Username', 'class':'login_box'})
        self.fields['password'].widget.attrs.update({'placeholder': ' Password', 'class':'login_box'})

class JoinForm(forms.Form):
    id = forms.CharField(label="ID ", max_length=20)
    password1 = forms.CharField(label="PASSWORD ", min_length=4, max_length=20, widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="PASSWORD(again) ", min_length=4, max_length=20, widget=forms.PasswordInput)
    email_address = forms.EmailField(label="Email Address ", error_messages={'invalid': '정확한 Email 주소를 입력해주세요.'})

    def clean_id(self):
        # get_user_model helper 함수를 통해 모델 클래스 참조
        User = auth.get_user_model()
        
        # ID 중복여부
        if User.objects.filter(username=self.cleaned_data['id']).exists():
            raise ValidationError('아이디가 이미 사용중입니다.')
        return self.cleaned_data['id']

    def clean_password2(self):
        # 패스워드 동일 체크
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError('비밀번호를 동일하게 입력해주십시오.')

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({'class': 'txtbox'})
        self.fields['password1'].widget.attrs.update({'class': 'txtbox'})
        self.fields['password2'].widget.attrs.update({'class': 'txtbox'})
        self.fields['email_address'].widget.attrs.update({'class': 'txtbox'})

class EditForm(forms.Form):
    password1 = forms.CharField(label="PASSWORD ", min_length=4, max_length=20, widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="PASSWORD(again) ", min_length=4, max_length=20, widget=forms.PasswordInput)
    email_address = forms.EmailField(label="Email Address ", error_messages={'invalid': '정확한 Email 주소를 입력해주세요.'})

    def clean_password2(self):
        # 패스워드 동일 체크
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError('비밀번호를 동일하게 입력해주십시오.')

        return self.cleaned_data
    
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)

        super(EditForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.initial['email_address'] = self.instance.email

        self.fields['password1'].widget.attrs.update({'class': 'txtbox'})
        self.fields['password2'].widget.attrs.update({'class': 'txtbox'})
        self.fields['email_address'].widget.attrs.update({'class': 'txtbox'})    
      
          
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number',)
        labels = {
            'phone_number' : 'Phone number '
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs.update({'class': 'txtbox'})
