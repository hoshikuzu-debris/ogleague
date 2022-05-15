from classic.models import Question, Answer
from django.http import JsonResponse, Http404
from django.db.models import Count, Q, Sum
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404
from classic.models import Answer, Favorite
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
import json

from classic.models import Question, QuestionCheck

@require_POST
@login_required
def check_question(request):
    data = json.loads(request.body)
    queryset = Question.objects.filter(
        was_checked=False,
        pk=data.get('question_id')
    ).exclude(
        Q(questioner=request.user) |
        Q(question_check__checker=request.user)
    )

    try:
        question = queryset.get()
    except Question.DoesNotExist:
        raise Http404(
            "No %s matches the given query." % queryset.model._meta.object_name
        )
    else:
        QuestionCheck.objects.create(
            question=question,
            checker=request.user,
            choice=data.get('choice')
        )
        max_question_checker = getattr(settings, 'MAX_QUESTON_CHECKER', 10)
        # お題のチャッカーの人数が規定に達したとき
        if QuestionCheck.objects.filter(
            question=question
        ).count() == max_question_checker:
            # チェッカーの2/3以上の賛成でお題出題が認められる <=> チェッカーの1/3以上の反対でお題が却下される
            # 0:いいね 1:う〜ん
            if question.question_checks.aggregate(Sum('choice'))['choice__sum'] >= max_question_checker // 3:
                question.was_checked = True
                question.save()
            else:
                question.was_checked = True
                question.is_safe = True
                question.save()
        d = {
            'success': True
        }
        return JsonResponse(d)