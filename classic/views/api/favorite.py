from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from classic.models import Answer, Favorite
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
import json

from classic.models import Question, QuestionCheck

@require_POST
@login_required
def post_favorite(request):
    print(request.body)
    data = json.loads(request.body)
    answer = get_object_or_404(Answer, pk=data.get('answer_id'))
    queryset = Favorite.objects.filter(
        answer=answer,
        user=request.user
    )
    if queryset.exists():
        favorite = queryset.get()
        favorite.delete()
    else:
        Favorite.objects.create(
            answer=answer,
            user=request.user
        )
    context = { 'answer': answer }
    content = render_to_string('classic/includes/favorite.html', context, request)
    d = {'content': content}
    return JsonResponse(d)