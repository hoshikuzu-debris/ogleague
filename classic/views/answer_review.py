import enum
import math
from pipes import Template
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, DetailView, RedirectView, UpdateView, FormView
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.db.models import F, Q

from classic.models import Question, Answer, Contest, Match, Level, AnswerReview
from classic.forms import AnswerForm, create_DynamicAnswerReviewForm


User = get_user_model()

class AnswerMarkTop(TemplateView):
    template_name = 'classic/answer_mark_top.html'

    def get_context_data(self, **kwargs):
        """Insert match into the context dict."""
        context = super().get_context_data(**kwargs)
        contest = get_object_or_404(
            Contest,
            is_held=True,
            is_marked=True,
            post_deadline__lte=timezone.now(),
            date_marked__gte=timezone.now(),
        )
        match_list = Match.objects.filter(
            contest=contest
        ).order_by('level__order')
        context.update({
            'contest': contest,
            'match_list': match_list,
        })
        return context


class AnswerMarkPost(LoginRequiredMixin, FormView):
    '''
        contestに紐づくanswers採点入力フォーム
    '''
    template_name = 'classic/answer_mark_post.html'


    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        # 自分が答えている場合は採点top画面にリダイレクトする
        match = self.kwargs['match']
        if User.objects.filter(
            pk=request.user.id,
            answer__match=match
        ).exists():
            messages.info(request, "自分が参加しているマッチの採点はできません")
            return redirect('classic:answer_mark_top')
        # 一度採点している場合は採点決定画面にリダイレクトする
        if User.objects.filter(
            pk=request.user.id,
            answer_review__answer__match=match
        ).exists():
            return redirect('classic:answer_mark_done', match.level.name)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        match = self.kwargs['match']
        self.request.session[f'mark_form_data_{match.id}'] = form.cleaned_data
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "採点を保存できませんでした")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """Insert match into the context dict."""
        context = super().get_context_data(**kwargs)
        context.update({
            'match': self.kwargs['match'],
            'question': Question.objects.filter(
                was_checked=False
            ).exclude(
                Q(questioner=self.request.user) |
                Q(question_check__checker=self.request.user)
            ).order_by(
                'id'
            ).first()
        })
        return context

    def get_form_class(self):
        match = self.kwargs['match']
        return create_DynamicAnswerReviewForm(match.id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            match = self.kwargs['match']
            kwargs['data'] = self.request.session.get(f'mark_form_data_{match.id}')
        return kwargs

    def get_success_url(self):
        return reverse('classic:answer_mark_confirm', kwargs={'level_name': self.kwargs.get('level_name')})

    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        super().setup(request, *args, **kwargs)
        level = get_object_or_404(
            Level,
            name=self.kwargs.get('level_name'),
        )
        self.kwargs['match'] = get_object_or_404(
            Match,
            contest__is_held=True,
            contest__is_marked=True,
            contest__post_deadline__lte=timezone.now(),
            contest__date_marked__gte=timezone.now(),
            level=level,
        )


class AnswerMarkConfirm(LoginRequiredMixin, FormView):
    '''
        contestに紐づくanswers採点確認フォーム
    '''
    template_name = 'classic/answer_mark_confirm.html'
    success_url = reverse_lazy('classic:answer_mark_top')

    def dispatch(self, request, *args, **kwargs):
        # 自分が答えている場合は採点top画面にリダイレクトする
        match = self.kwargs['match']
        if User.objects.filter(
            pk=request.user.id,
            answer__match=match
        ).exists():
            messages.info(request, "自分が参加しているマッチの採点はできません")
            return redirect('classic:answer_mark_top')
        # 一度採点している場合は採点決定画面にリダイレクトする
        if User.objects.filter(
            pk=request.user.id,
            answer_review__answer__match=match
        ).exists():
            messages.info(request, "すでに採点が済んでいます")
            return redirect('classic:answer_mark_done', match.level.name)
        # セッション切れや、セッションが空でURL直接入力したら入力画面にリダイレクト
        if self.kwargs['form_data'] is None:
            return redirect('classic:answer_mark_top')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        match = self.kwargs['match']
        form_data = self.kwargs['form_data']
        answer_list = Answer.objects.filter(match=match)
        for answer in answer_list:
            answer_review = AnswerReview.objects.create(
                answer=answer,
                reviewer=self.request.user,
                point=form_data[f'point_{answer.id}'],
                comment=form_data[f'comment_{answer.id}']
            )
            answer.score = F('score') + answer_review.point
            answer.save()
        for index, answer in enumerate(answer_list.order_by('-score')):
            answer.rank = index + 1
            answer.save()
        self.request.session.pop(f'mark_form_data_{match.id}')
        messages.success(self.request, "採点を完了しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "採点を保存できませんでした")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """Insert match into the context dict."""
        context = super().get_context_data(**kwargs)
        context['match'] = self.kwargs['match']
        return context

    def get_form_class(self):
        match = self.kwargs['match']
        return create_DynamicAnswerReviewForm(match.id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('GET', 'POST', 'PUT'):
            match = self.kwargs['match']
            kwargs.update({
                'data': self.request.session.get(f'mark_form_data_{match.id}')
            })
        return kwargs

    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        super().setup(request, *args, **kwargs)
        level = get_object_or_404(
            Level,
            name=self.kwargs.get('level_name'),
        )
        match = get_object_or_404(
            Match,
            contest__is_held=True,
            contest__is_marked=True,
            contest__post_deadline__lte=timezone.now(),
            contest__date_marked__gte=timezone.now(),
            level=level,
        )
        self.kwargs['match'] = match
        self.kwargs['form_data'] = request.session.get(f'mark_form_data_{match.id}')


class AnswerMarkDone(LoginRequiredMixin, DetailView):
    template_name = 'classic/answer_mark_done.html'

    def dispatch(self, request, *args, **kwargs):
        # 自分が答えている場合は採点top画面にリダイレクトする
        match = self.kwargs['match']
        if User.objects.filter(
            pk=request.user.id,
            answer__match=match
        ).exists():
            messages.info(request, "自分が参加しているマッチの採点はできません")
            return redirect('classic:answer_mark_top')
        # 採点が済んでいない場合は採点入力画面にリダイレクトする
        if not User.objects.filter(
            pk=request.user.id,
            answer_review__answer__match=match
        ).exists():
            messages.info(request, "まだ採点が済んでいません")
            return redirect('classic:answer_mark_post', match.level.name)

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.kwargs['match']

    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        super().setup(request, *args, **kwargs)
        level = get_object_or_404(
            Level,
            name=self.kwargs.get('level_name'),
        )
        match = get_object_or_404(
            Match,
            contest__is_held=True,
            contest__is_marked=True,
            contest__post_deadline__lte=timezone.now(),
            contest__date_marked__gte=timezone.now(),
            level=level,
        )
        self.kwargs['match'] = match