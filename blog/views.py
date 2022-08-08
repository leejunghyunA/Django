# from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# 요청을 받으면 포스트에 받은객체를 rendering해서 넣어줌
class PostList(ListView):
    model = Post
    ordering = '-pk'

class PostDetail(DetailView):
    model = Post
# Create your views here.

# #FBV 방법
# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#     # post에 있는 객체를 모두 가져옴 ('-pk'는 역순)

#     return render(
#         request, 
#         'blog/index.html',
#         {
#             'posts' : posts,
#         }
#     )
# 
#single_post_page 함수 정의
# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)

#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post':post,
#         }
#     )
