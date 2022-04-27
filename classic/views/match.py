from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from classic.models import Question, Answer, Contest, Match
from classic.forms import AnswerForm


class MatchDetail(DetailView):
    template_name = 'classic/match_detail.html'

    def get_object(self, queryset=None):
        match = get_object_or_404(
            Match,
            contest__was_marked=True,
            contest__id=self.kwargs.get('contest_id'),
            level__name=self.kwargs.get('level_name'),
        )
        return match