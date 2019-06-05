from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.main_page, name= 'main_page'),
    path('login/', views.login_page, name='login_page'),
    path('login/validate', views.login_validate, name='login_validate'),
    path('logout/', views.logout, name='logout'),
    path('join/', views.join_page, name='join_page'),
]
