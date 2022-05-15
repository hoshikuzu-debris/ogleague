from django import forms
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminTextareaWidget, AdminTextInputWidget
from django.shortcuts import get_object_or_404

from .models import Question, Answer, AnswerReview, AnswerComment, Favorite, QuestionCheck, Contest, Level, Match

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


# 管理サイト用のFavoriteForm
class QuestionCheckAdminForm(ModelForm):
    class Meta:
        model = QuestionCheck
        fields = '__all__'


# 管理サイト用ContestForm
class ContestAdminForm(ModelForm):
    class Meta:
        model = Contest
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


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text',]
        widgets = {
            'text': forms.Textarea(attrs={'rows': '3'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ""


class AnswerReviewForm(forms.Form):
    pass


# 管理サイト用のAnswerReviewForm
class AnswerReviewAdminForm(ModelForm):
    class Meta:
        model = AnswerReview
        fields = '__all__'


def create_DynamicAnswerReviewForm(match_id):
    match = get_object_or_404(Match, pk=match_id)
    form_item = {}

    # create answer_review form objects
    for answer in match.answers.all().order_by('?'):
        form_item.update(
            {
                f'point_{answer.id}': forms.TypedChoiceField(
                        label=answer.text, label_suffix='', choices=AnswerReview.POINT_CHOICES, initial=0, coerce=int, empty_value=None,
                        widget=forms.RadioSelect(attrs={'class': 'btn-check', 'autocomplete': 'off'}),
                    ),
                # f'comment_{answer.id}': forms.CharField(
                #         label='', label_suffix='', max_length=20, required=False,
                #         widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '20文字以内'}),
                #     ),
            }
        )

    # ReviewFormを継承した，fieldオブジェクトにform_itemを代入したDynamicReviewFormを作成
    DynamicReviewForm = type('DynamicReviewForm', (AnswerReviewForm, ), form_item)

    return DynamicReviewForm


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'image', ]
        widgets = {
            'text': forms.Textarea(attrs={'rows': '3'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ""