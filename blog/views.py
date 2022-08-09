# from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category

# 요청을 받으면 포스트에 받은객체를 rendering해서 넣어줌
class PostList(ListView):
    model = Post
    ordering = '-pk'

    # category 추가 (get_context_data 내장 함수 오버라이딩)
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        return context
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
