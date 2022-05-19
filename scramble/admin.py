from django.contrib import admin
from django.contrib.auth import get_user_model

from .forms import AnswerReviewAdminForm, AnswerCommentAdminForm, QuestionAdminForm, AnswerAdminForm, FavoriteAdminForm, LevelAdminForm, MatchAdminForm
from .models import Question, Answer, AnswerReview, AnswerComment, Favorite, Level, Match
from common.models import Profile


User = get_user_model()

# Register your models here.
class AnswerAdminInline(admin.TabularInline):
    model = Answer
    form = AnswerAdminForm
    ordering = ['-rank', ]
    extra = 1


class AnswerReviewAdminInline(admin.TabularInline):
    model = AnswerReview
    form = AnswerReviewAdminForm
    ordering = ['-id', ]
    extra = 1

class AnswerCommentAdminInline(admin.TabularInline):
    model = AnswerComment
    form = AnswerCommentAdminForm
    ordering = ['-id', ]
    extra = 1


class FavoriteAdminInline(admin.TabularInline):
    model = Favorite
    form = FavoriteAdminForm
    extra = 1


class MatchAdminInline(admin.TabularInline):
    model =  Match
    form =  MatchAdminForm
    classes = ['collapse', ]
    extra =0


class ProfileAdminInline(admin.TabularInline):
    model =  Profile
    fields = ['user']
    classes = ['collapse', ]
    can_delete = False
    readonly_fields = ['user',]    # この行を追加
    extra = 0

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['questioner', 'image', 'text']}),
        ('状態', {'fields': [("was_checked", "is_safe", "was_asked",), ],}),
    ]
    form = QuestionAdminForm
    list_display = ("id", "text", "was_checked", "is_safe", "was_asked",)
    list_filter = ("was_checked", "is_safe", "was_asked",)
    search_fields = ("text",)
    ordering = ("-id", )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    form = AnswerAdminForm
    list_display = ("match", "rank", "score", "text", "panellist")
    search_fields = ("text",)
    ordering = ("-match", )
    inlines = [AnswerReviewAdminInline, AnswerCommentAdminInline, FavoriteAdminInline, ]


@admin.register(AnswerReview)
class AnswerReviewAdmin(admin.ModelAdmin):
    form = AnswerReviewAdminForm
    list_display = ("answer", "reviewer","point",)

@admin.register(AnswerComment)
class AnswerCommentAdmin(admin.ModelAdmin):
    form = AnswerCommentAdminForm
    list_display = ("answer", "commentator","text",)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    form = FavoriteAdminForm
    list_display = ("answer", "user", "timestamp")

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    form = LevelAdminForm
    #inlines = [MatchAdminInline,  ProfileAdminInline]

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    form = MatchAdminForm
    list_display = ['level', 'question']
    inlines = [AnswerAdminInline, ]