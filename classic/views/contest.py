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


class ContestList(ListView):
    model = Contest
    template_name = 'classic/contest_list.html'
    queryset = Contest.objects.filter(was_marked=True)


class ContestDetail(DetailView):
    model = Contest
    template_name = 'classic/contest_detail.html'
    pk_url_kwarg = 'contest_id'
    queryset = Contest.objects.filter(was_marked=True)


class ContestRedirect(LoginRequiredMixin, RedirectView):
    '''
        現在のコンテストが出題中か採点中なのか判別してリダイレクトする
    '''
    def get_redirect_url(self, *args, **kwargs):
        url = None
        # 現在，出題中の場合
        if Contest.objects.filter(
            is_held=True,
            is_asked=True,
            date_asked__lte=timezone.now(),
            post_deadline__gte=timezone.now(),
        ).exists():
            url = reverse('classic:answer_post')
        # 現在，採点中の場合
        elif Contest.objects.filter(
            is_held=True,
            is_marked=True,
            post_deadline__lte=timezone.now(),
            date_marked__gte=timezone.now(),
        ).exists():
            url = reverse('classic:answer_mark_top')

        return url
