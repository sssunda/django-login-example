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
            # get_user_model helper 함수를 통해 모델 클래스 참조
            User = auth.get_user_model()

            username = form_data.cleaned_data['id']
            password = form_data.cleaned_data['password']
            password_check = form_data.cleaned_data['password_check']

            # ID 중복여부
            if User.objects.filter(username=username).exists():
                return render(request, 'join_page.html', {'join_data':form_data, 'join_errors':'아이디가 이미 사용중입니다.'}) 
                
            # PASSWORD 동일한지 체크    
            if password==password_check:
                User.objects.create_user(username=username, password=password)
                return redirect('/')
            return render(request, 'join_page.html', {'join_data':form_data, 'join_errors':'비밀번호를 동일하게 입력해주십시오.'})
    else :
        form_data = JoinForm()

    return render(request, 'join_page.html', {'join_data':form_data})