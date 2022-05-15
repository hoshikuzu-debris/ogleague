from classic.models import Question, Answer
from django.http import JsonResponse, Http404
from django.db.models import Count, Q, Sum
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404
from classic.models import Answer, Favorite
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
import json

from classic.models import Question, QuestionCheck, AnswerComment

@require_POST
@login_required
def post_comment(request):
    data = json.loads(request.body)
    answer = get_object_or_404(Answer, pk=data.get('answer_id'))
    text = data.get('text')
    AnswerComment.objects.create(
        answer=answer,
        commentator=request.user,
        text=text
    )
    context = { 'answer': answer }
    content = render_to_string('classic/includes/answer_comment.html', context, request)
    d = {'content': content}
    return JsonResponse(d)