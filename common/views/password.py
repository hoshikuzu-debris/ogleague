from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)

from ..forms import (
    MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
)


class PasswordChange(PasswordChangeView):
    '''パスワード変更ビュー'''
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('common:password_change_done')
    template_name = 'common/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    '''パスワード変更しました'''
    template_name = 'common/password_change_done.html'


class PasswordReset(PasswordResetView):
    '''パスワード忘れた人に変更用URLの送付ページ'''
    subject_template_name = 'common/mail/password_reset/subject.txt'
    email_template_name = 'common/mail/password_reset/message.txt'
    template_name = 'common/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('common:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    '''パスワード忘れた人に変更用URLを送りましたページ'''
    template_name = 'common/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    '''パスワード忘れた人が新パスワード入力ページ'''
    form_class = MySetPasswordForm
    success_url = reverse_lazy('common:password_reset_complete')
    template_name = 'common/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    '''パスワード忘れた人が新パスワード設定しましたページ'''
    template_name = 'common/password_reset_complete.html'

