# from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# 요청을 받으면 포스트에 받은객체를 rendering해서 넣어줌
class PostList(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = '-pk'

class PostDetail(DetailView):
    model = Post
# Create your views here.
