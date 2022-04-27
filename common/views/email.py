from django.conf import settings
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from common.forms import EmailChangeForm


class EmailChange(LoginRequiredMixin, generic.FormView):
    '''メールアドレスの変更'''
    template_name = 'common/email_change_form.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }

        subject = render_to_string('common/mail/email_change/subject.txt', context)
        message = render_to_string('common/mail/email_change/message.txt', context)
        send_mail(subject, message, None, [new_email])

        return redirect('common:email_change_done')


class EmailChangeDone(LoginRequiredMixin, generic.TemplateView):
    '''メールアドレスの変更メールを送ったよ'''
    template_name = 'common/email_change_done.html'


class EmailChangeComplete(LoginRequiredMixin, generic.TemplateView):
    '''リンクを踏んだ後に呼ばれるメアド変更ビュー'''
    template_name = 'common/email_change_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60)  # デフォルトでは1時間以内

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは間違いなし
        else:
            # User.objects.get(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)

