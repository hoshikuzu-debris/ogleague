from django.contrib.auth.views import LoginView, LogoutView

from common.forms import LoginForm


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'common/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'common/index.html'