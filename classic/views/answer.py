from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, RedirectView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import Http404

from classic.models import Question, Answer, Contest, Match
from classic.forms import AnswerForm


User = get_user_model()

class AnswerPost(LoginRequiredMixin, CreateView):
    '''
    クラスベースビューで書こうとしたらこうなる
    '''
    model = Answer
    form_class = AnswerForm
    template_name = 'classic/answer_post.html'
    success_url = reverse_lazy('classic:answer_edit')


    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        super().setup(request, *args, **kwargs)
        self.kwargs['match'] = get_object_or_404(
            Match,
            contest__is_held=True,
            contest__is_asked=True,
            contest__date_asked__lte=timezone.now(),
            contest__post_deadline__gte=timezone.now(),
            level=request.user.profile.classic_level,
        )

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        # 一度答えている場合は編集画面にリダイレクトする
        if User.objects.filter(
            pk=request.user.id,
            answer__match=self.kwargs['match']
        ).exists():
            return redirect('classic:answer_edit')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.panellist = self.request.user
        form.instance.match = self.kwargs['match']
        messages.success(self.request, "回答を投稿しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        # バリデーションに失敗した時
        messages.warning(self.request, "回答を投稿できませんでした")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """Insert match into the context dict."""
        if 'match' not in kwargs:
            kwargs['match'] = self.kwargs['match']
        return super().get_context_data(**kwargs)


class AnswerEdit(LoginRequiredMixin, UpdateView):
    '''
    クラスベースビューで書こうとしたらこうなる
    '''
    model = Answer
    form_class = AnswerForm
    template_name = 'classic/answer_edit.html'
    success_url = reverse_lazy('classic:index')

    def form_valid(self, form):
        messages.success(self.request, "回答を投稿しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        # バリデーションに失敗した時
        messages.warning(self.request, "回答を投稿できませんでした")
        return super().form_invalid(form)

    def get_object(self, queryset=None):
        answer = get_object_or_404(
            Answer,
            match__contest__is_held=True,
            match__contest__is_asked=True,
            match__contest__date_asked__lte=timezone.now(),
            match__contest__post_deadline__gte=timezone.now(),
            match__level=self.request.user.profile.classic_level,
            panellist=self.request.user,
        )
        return answer
