from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('user_info/', views.user_info, name='user_info'),
    path('logout/', views.logout, name='logout'),
    path('login_for_modal/', views.login_for_modal, name='login_for_modal'),
    path('register/', views.register, name='register'),
    path('change_nickname/', views.change_nickname, name='change_nickname'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
    path('get_captcha/', views.get_captcha, name='get_captcha'),
    path('login_by_qq/', views.login_by_qq, name='login_by_qq'),
    path('bind_qq/', views.bind_qq, name='bind_qq'),
    path('create_user_by_qq/', views.create_user_by_qq, name='create_user_by_qq'),
    ]
