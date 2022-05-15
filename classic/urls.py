from django.urls import path

from . import views


app_name = 'classic'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('contest/', views.ContestRedirect.as_view(), name='contest_redirect'),
    path('contest/answer/', views.AnswerPost.as_view(), name='answer_post'),
    path('contest/answer/edit/', views.AnswerEdit.as_view(), name='answer_edit'),
    path('contest/mark/', views.AnswerMarkTop.as_view(), name='answer_mark_top'),
    path('contest/mark/post/<slug:level_name>/', views.AnswerMarkPost.as_view(), name='answer_mark_post'),
    path('contest/mark/confirm/<slug:level_name>/', views.AnswerMarkConfirm.as_view(), name='answer_mark_confirm'),
    path('contest/mark/done/<slug:level_name>/', views.AnswerMarkDone.as_view(), name='answer_mark_done'),
    path('contest/results/', views.ContestList.as_view(), name='contest_list'),
    path('contest/results/<int:contest_id>/', views.ContestDetail.as_view(), name='contest_detail'),
    path('contest/results/<int:contest_id>/<slug:level_name>/', views.MatchDetail.as_view(), name='match_detail'),
    path('gallery/', views.GalleryTop.as_view(), name='gallery_top'),
    path('gallery/<int:answer_id>/', views.GalleryDetail.as_view(), name='gallery_detail'),
    path('question/post/', views.QuestionPost.as_view(), name='question_post'),
    path('question/check/', views.QuestionCheck.as_view(), name='question_check'),

    #path('api/ajax-post-search/', views.ajax_post_search, name='ajax_post_search'),
    path('api/post-favorite/', views.api.post_favorite, name='api_post_favorite'),
    path('api/post-comment/', views.api.post_comment, name='api_post_comment'),
    #path('api/ajax-sort-answer/', views.ajax_sort_answer, name='ajax_sort_answer'),
    path('api/check-question/', views.api.check_question, name='api_check_question'),
]