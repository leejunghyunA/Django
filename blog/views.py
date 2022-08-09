from django.shortcuts import render
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
    
# 카테고리 페이지(해당 카테고리 포스트만 보여주도록)
def category_page(request, slug):

    # 카테고리 미분류일 때
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        # 동일한 slug를 갖는 카테고리를 불러옴(category변수에 저장)
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
            # post_list와 동일한 출력모양(템플릿 설정)
        'blog/post_list.html',
        {
            # post_list에 context 부분 정의
            'post_list': post_list,
            'categories':Category.objects.all(),
            'no_category_post_count':Post.objects.filter(category=None).count(),
            'category':category,
        }
    )

class PostDetail(DetailView):
    model = Post

    # category 추가 (get_context_data 내장 함수 오버라이딩)
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        return context
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
