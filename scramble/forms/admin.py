from django import forms
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminTextareaWidget, AdminTextInputWidget

from scramble.models import Question, Answer, AnswerReview, AnswerComment, Favorite, Level, Match

# 管理サイト用のQuestionForm
class QuestionAdminForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__' # 結局のところ，Metaで定義したfields属性は無視されるらしい
        widgets = {
            'text': AdminTextareaWidget(),
        }


# 管理サイト用のAnswerForm
class AnswerAdminForm(ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'
        widgets = {
            'text': AdminTextInputWidget(),
        }


class AnswerCommentAdminForm(ModelForm):
    class Meta:
        model = AnswerComment
        fields = '__all__'

# 管理サイト用のFavoriteForm
class FavoriteAdminForm(ModelForm):
    class Meta:
        model = Favorite
        fields = '__all__'


# 管理サイト用のLevelForm
class LevelAdminForm(ModelForm):
    class Meta:
        model = Level
        fields = '__all__'


# 管理サイト用のMatchForm
class MatchAdminForm(ModelForm):
    class Meta:
        model = Match
        fields = '__all__'


# 管理サイト用のAnswerReviewForm
class AnswerReviewAdminForm(ModelForm):
    class Meta:
        model = AnswerReview
        fields = '__all__'