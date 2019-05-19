import random
import string
import time
from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from .models import Profile, OAuthRelationship
from .forms import LoginForm, RegForm, ChangeNicknameForm, BindEmailForm, ChangePasswordForm, ForgotPasswordForm, \
    BindQQForm
from geetest import GeetestLib


captcha_id = "b46d1900d0a894591916ea94ea91bd2c"
private_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    context = {
        'login_form': login_form
    }
    return render(request, 'login.html', context)


def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            # 删除session
            del request.session['register_code']
            # 登陆用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()
    context = {
        'reg_form': reg_form,
    }
    return render(request, 'register.html', context)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def user_info(request):
    context = {}
    return render(request, 'user_info.html', context)


def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()
    context = {
        'page_title': '修改昵称',
        'form_title': '修改昵称',
        'submit_text': '修改',
        'form': form,
    }
    return render(request, 'form.html', context)


def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 删除session
            del request.session['bind_email_code']
            return redirect(redirect_to)
    else:
        form = BindEmailForm()
    context = {
        'page_title': '绑定邮箱',
        'form_title': '绑定邮箱',
        'submit_text': '绑定',
        'form': form,
    }
    return render(request, 'bind_email.html', context)


def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for').strip()
    data = {}
    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        request.session[send_for] = code
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
            # 发送邮件
            send_mail(
                '绑定邮箱',
                '验证码: %s' % code,
                '1753936488@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def change_password(request):
    if request.method == 'POST':
        change_password_form = ChangePasswordForm(request.POST, user=request.user)
        if change_password_form.is_valid():
            new_password = change_password_form.cleaned_data['new_password']
            request.user.set_password(new_password)
            request.user.save()
            auth.logout(request)
            return redirect(reverse('home'))
    else:
        change_password_form = ChangePasswordForm()
    context = {
        'page_title': '修改密码',
        'form_title': '修改密码',
        'submit_text': '修改',
        'form': change_password_form,
    }
    return render(request, 'change_password.html', context)


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            # 删除session
            del request.session['forgot_password_code']
            return redirect(reverse('login'))
    else:
        form = ForgotPasswordForm()
    context = {
        'page_title': '忘记密码',
        'form_title': '重置密码',
        'submit_text': '重置',
        'form': form,
    }
    return render(request, 'forgot_password.html', context)


def get_captcha(request):
    user_id = 'test'
    gt = GeetestLib(captcha_id, private_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def login_by_qq(request):
    state = request.GET.get('state')
    code = request.GET.get('code')
    if state != settings.QQ_STATE:
        raise Exception('state error')
    params = {
        'grant_type': 'authorization_code',
        'client_id': settings.QQ_APP_ID,
        'client_secret': settings.QQ_APP_KEY,
        'code': code,
        'redirect_uri': settings.QQ_REDIRECT_URL,
    }
    response = urlopen('https://graph.qq.com/oauth2.0/token?'+urlencode(params))
    data = response.read().decode('utf8')
    access_token = parse_qs(data)['access_token'][0]

    #  获取openID
    response = urlopen('https://graph.qq.com/oauth2.0/me?access_token=' + access_token)
    data = response.read().decode('utf8')
    import json
    openid = json.loads(data[10:-4])['openid']
    #  判断openid是否有关联用户
    if OAuthRelationship.objects.filter(openid=openid, oauth_type=0).exists():
        relationship = OAuthRelationship.objects.get(openid=openid, oauth_type=0)
        auth.login(request, relationship.user)
        return redirect(reverse('home'))
    else:
        # 获取用户信息
        request.session['openid'] = openid
        params = {
            'access_token': access_token,
            'oauth_consumer_key': settings.QQ_APP_ID,
            'openid': openid,
        }
        url = 'https://graph.qq.com/user/get_user_info?' + urlencode(params)
        response = urlopen(url)
        data = response.read().decode('utf8')
        import json
        params = {
            'nickname': json.loads(data)['nickname'],
            'avatar': json.loads(data)['figureurl_qq_1'],
        }
        return redirect(reverse('bind_qq')+'?'+urlencode(params))
    # import pdb
    # pdb.set_trace()


def bind_qq(request):
    if request.method == 'POST':
        bind_qq_form = BindQQForm(request.POST)
        if bind_qq_form.is_valid():
            user = bind_qq_form.cleaned_data['user']
            openid = request.session.pop('openid')
            # 记录关系
            relationship = OAuthRelationship()
            relationship.user = user
            relationship.openid = openid
            relationship.oauth_type = 0
            relationship.save()
            # 登陆
            auth.login(request, user)
            return redirect(reverse('home'))
    else:
        bind_qq_form = BindQQForm()
    context = {
        'bind_qq_form': bind_qq_form,
        'nickname': request.GET.get('nickname'),
        'avatar': request.GET.get('avatar'),
    }
    return render(request, 'bind_qq.html', context)


def create_user_by_qq(request):
    # 创建随机用户
    username = str(int(time.time()))
    password = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    user = User.objects.create_user(username, '', password)
    openid = request.session.pop('openid')
    nickname = request.GET['nickname']
    profile = Profile()
    profile.user = user
    profile.nickname = nickname
    profile.save()
    # 记录关系
    relationship = OAuthRelationship()
    relationship.user = user
    relationship.openid = openid
    relationship.oauth_type = 0
    relationship.save()
    # 登陆
    auth.login(request, user)
    return redirect(reverse('home'))
