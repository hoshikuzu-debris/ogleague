from django.contrib import admin
from django.contrib.auth import get_user_model

from .forms import AnswerReviewAdminForm, QuestionAdminForm, AnswerAdminForm, FavoriteAdminForm, QuestionCheckAdminForm, ContestAdminForm, LevelAdminForm, MatchAdminForm
from .models import Question, Answer, AnswerReview, Favorite, QuestionCheck, Contest, Level, Match
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


class FavoriteAdminInline(admin.TabularInline):
    model = Favorite
    form = FavoriteAdminForm
    extra = 1


class QuestionCheckAdminInline(admin.TabularInline):
    model = QuestionCheck
    form = QuestionCheckAdminForm
    classes = ['collapse', ]
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
    inlines = [QuestionCheckAdminInline, ]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    form = AnswerAdminForm
    list_display = ("match", "rank", "score", "text", "panellist")
    search_fields = ("text",)
    ordering = ("-match", )
    inlines = [AnswerReviewAdminInline, FavoriteAdminInline, ]


@admin.register(AnswerReview)
class AnswerReviewAdmin(admin.ModelAdmin):
    form = AnswerReviewAdminForm
    list_display = ("answer", "reviewer","point",)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    form = FavoriteAdminForm
    list_display = ("answer", "user", "timestamp")


@admin.register(QuestionCheck)
class QuestionCheckAdmin(admin.ModelAdmin):
    form = QuestionCheckAdminForm
    list_display = ("question", "checker", "choice")
    search_fields = ("question", "checker" )


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    form = ContestAdminForm
    list_display = ("id", "is_held", "is_asked", "is_marked", "was_marked")
    inlines = [MatchAdminInline, ]
    # search_fields = ("question", "checker" )


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    form = LevelAdminForm
    inlines = [MatchAdminInline,  ProfileAdminInline]


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    form = MatchAdminForm
    list_display = ['contest', 'level', 'question']
    inlines = [AnswerAdminInline, ]