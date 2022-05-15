from classic.models import Question, Answer
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
class GalleryTop(ListView):
    template_name = 'classic/gallery_top.html'
    queryset = Answer.objects.filter(
        match__contest__was_marked=True,
    )


class GalleryDetail(DetailView):
    # model = Answer
    template_name = 'classic/gallery_detail.html'
    pk_url_kwarg = 'answer_id'
    queryset = Answer.objects.filter(
        match__contest__was_marked=True,
    )