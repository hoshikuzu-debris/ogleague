from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.db.models import Count
import datetime
from classic.models import Contest, Match, Level, Question, Answer


def after_a_week():
    return timezone.now() + datetime.timedelta(weeks=1)


class Command(BaseCommand):
    help = 'コンテストをセットします'

    def handle(self, *args, **options):
        # 現在，出題中の場合
        if Contest.objects.filter(
            is_held=True,
            is_asked=True,
        ).exists():
            current_contest = Contest.objects.filter(
                is_held=True,
                is_asked=True,
            ).get()
            current_contest.is_asked = False
            current_contest.is_marked = True
            current_contest.post_deadline = timezone.now()
            current_contest.date_marked = after_a_week()
            current_contest.save()
            self.stdout.write(self.style.SUCCESS(
                'コンテストの回答期間が終了しました.'
                'コンテストの採点期限は1週間後です.'
            ))
        # 現在，採点中の場合とコンテストが開催されていない場合
        else:
            # 現在，採点中の場合のみ
            if Contest.objects.filter(
                is_held=True,
                is_marked=True,
            ).exists():
                current_contest = Contest.objects.filter(
                    is_held=True,
                    is_marked=True,
                ).get()
                current_contest.is_held = False
                current_contest.is_marked = False
                current_contest.was_marked = True
                current_contest.date_marked = timezone.now()
                current_contest.save()
            safe_question_list = Question.objects.filter(
                is_safe=True,
                was_asked=False
            ).order_by('id')
            level_list = Level.objects.all()
            if safe_question_list.count() >= level_list.count():
                next_contest = Contest.objects.create(
                    is_held=True,
                    is_asked=True,
                )
                for level in level_list:
                    question = safe_question_list.first()
                    Match.objects.create(
                        question=question,
                        contest=next_contest,
                        level=level
                    )
                    question.was_asked = True
                    question.save()
                self.stdout.write(self.style.SUCCESS(
                    'コンテストの採点期間が終了しました.'
                    '次のコンテストの回答期限は1週間後です.'
                ))
            else:
                raise CommandError('出題可能なお題の数が不足しています.')

