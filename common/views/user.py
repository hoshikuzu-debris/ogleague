from django.conf import settings
from django.shortcuts import redirect, resolve_url, render, get_object_or_404
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponseBadRequest
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from common.forms import MyUserCreationForm, UserUpdateForm, ProfileUpdateForm

from classic.models import Answer, Level


User = get_user_model()


class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'common/signup.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('common/mail/signup/subject.txt', context)
        message = render_to_string('common/mail/signup/message.txt', context)

        user.email_user(subject, message)
        return redirect('common:signup_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録した後の画面"""
    template_name = 'common/signup_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'common/signup_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60)  # デフォルトでは1時間以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    login(request, user)
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class UserSettingsList(LoginRequiredMixin, generic.TemplateView):
    template_name = 'common/user_settings_list.html'


class UserSettingsUpdate(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'common/user_settings_form.html'

    def get_success_url(self):
        return resolve_url('common:user_settings_list')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        ''' バリデーションを通った時 '''
        messages.success(self.request, "ユーザー情報を更新しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        ''' バリデーションに失敗した時 '''
        messages.warning(self.request, "ユーザー情報を更新できませんでした")
        return super().form_invalid(form)


@login_required
def user_settings_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, "ユーザー情報を更新しました")
            return redirect('common:user_settings_update')
        else:
            messages.warning(request, "ユーザー情報を更新できませんでした")

    # GETのとき
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile) # 既に保存してあるデータを引っ張ってきてformをテンプレートへ渡す

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'common/user_settings_form.html', context)


class UserList(generic.ListView):
    '''ユーザー一覧'''
    model = User
    ordering = ('profile', 'username', )
    paginate_by = 15
    template_name = 'common/user_list.html'
    # context_object_name = 'player_list'
    # queryset = User.objects.order_by('username')

# class UserList(generic.TemplateView):
    # '''ユーザー一覧'''
    # template_name = 'common/user_list.html'

    # def get_context_data(self, **kwargs):
        # """Insert match into the context dict."""
        # context = super().get_context_data(**kwargs)
        # player_list = {}
        # for level in Level.objects.order_by('order'):
            # player_list[level] = User.objects.filter(
                # profile__classic_level=level
            # ).order_by('username')
        # context['player_list'] = player_list
        # return context

class UserDetail(generic.DetailView):
    context_object_name = 'player'
    model = User
    template_name = 'common/user_detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer_list'] = Answer.objects.filter(
            panellist=self.object,
            match__contest__was_marked=True
        ).order_by('-date_answered')
        return context
