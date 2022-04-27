from django.views import generic
from django.db.models import F, Q

from classic.models import Question, Answer, Contest, Match, Level, AnswerReview


# Create your views here.
class QuestionCheck(generic.TemplateView):
    template_name = 'classic/question_check.html'

    def get_context_data(self, **kwargs):
        """Insert match into the context dict."""
        context = super().get_context_data(**kwargs)
        context['question'] = Question.objects.filter(
            was_checked=False
        ).exclude(
            Q(questioner=self.request.user) |
            Q(question_check__checker=self.request.user)
        ).order_by(
            'id'
        ).first()
        return context