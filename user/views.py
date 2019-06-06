from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import LoginForm, JoinForm, ProfileForm
from django.contrib import auth
from .models import Profile

# 메인 페이지
def main_page(request):
    return render(request, 'main.html', {})

# 로그인 페이지
def login_page(request):
    login_data = LoginForm()
    return render(request, 'login_page.html', {'login_data':login_data})

# 로그인 유효성 검사
def login_validate(request):
    login_data = LoginForm(request.POST)

    if login_data.is_valid():
        user = auth.authenticate(username=request.POST['id'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect('/')

        error_message= '사용자 ID 또는 비밀번호를 잘못입력하였습니다.'
        return render(request, 'login_page.html', {'login_data':login_data,'login_errors':error_message})
    error_message= '로그인 폼이 이상합니다.개발자에게 연락하시길 바랍니다.'
    return render(request, 'login_page.html', {'login_data':login_data,'login_errors':error_message})

# 로그아웃   
def logout(request):
    auth.logout(request)
    return redirect('/')

# 회원가입 페이지        
def join_page(request):
    if request.method =='POST':
        form_data = JoinForm(request.POST)
        
        if form_data.is_valid():
            # get_user_model helper 함수를 통해 모델 클래스 참조
            User = auth.get_user_model()

            username = form_data.cleaned_data['id']
            password = form_data.cleaned_data['password']
              
            User.objects.create_user(username=username, password=password)

            return redirect('/')
            
    else :
        form_data = JoinForm()
        profile_data = ProfileForm()

    return render(request, 'join_page.html', {'join_data':form_data, 'profile_data':profile_data})

# 개인정보 수정 페이지
def edit_user_info(request):
    # User 모델 클래스 가져오기
    User = auth.get_user_model()
    
    # 로그인된 user 정보 가져오기
    user_info = get_object_or_404(User, username = request.user.username)    

    if request.method =='POST':
        form_data = JoinForm(request.POST,instance = user_info)
        profile_form = ProfileForm(request.POST, instance = user_info.profile)

        if form_data.is_valid() and profile_form.is_valid():
            password = form_data.cleaned_data['password']
            email_address = form_data.cleaned_data['email_address']
            phone_number = profile_form.cleaned_data['phone_number']

            user_info.set_password(password)
            user_info.email = email_address
            user_info.profile.phone_number = phone_number

            user_info.save()

            user = auth.authenticate(username=request.user.username, password=password)
            auth.login(request, user)

            return redirect('/')
    
    form_data = JoinForm(instance = user_info)
    profile_form = ProfileForm(instance = user_info.profile)

    return render(request, 'edit_user.html', {'form_data':form_data, 'profile_form':profile_form})