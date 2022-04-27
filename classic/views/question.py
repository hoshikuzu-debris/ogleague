from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy

from classic.models import Question
from classic.forms import QuestionForm


class QuestionPost(LoginRequiredMixin, CreateView):
    '''
    Question投稿フォーム
    '''
    model = Question
    form_class = QuestionForm
    template_name = 'classic/question_post_form.html'
    success_url = reverse_lazy('classic:index')

    def form_valid(self, form):
        form.instance.questioner = self.request.user
        messages.success(self.request, "お題を投稿しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        # バリデーションに失敗した時
        messages.warning(self.request, "お題を投稿できませんでした")
        return super().form_invalid(form)