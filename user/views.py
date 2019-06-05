from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, JoinForm
from django.contrib import auth

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
    
def logout(request):
    auth.logout(request)
    return redirect('/')
        
def join_page(request):
    if request.method =='POST':
        form_data = JoinForm(request.POST)
        
        if form_data.is_valid():
            username = form_data.cleaned_data['id']
            password = form_data.cleaned_data['password']
            # get_user_model helper 함수를 통해 모델 클래스 참조
            User = auth.get_user_model()
            User.objects.create_user(username=username, password=password)

            return redirect('/')
    else :
        form_data = JoinForm()

    return render(request, 'join_page.html', {'join_data':form_data})