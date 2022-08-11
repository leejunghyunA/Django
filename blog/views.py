from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView

# Login->로그인했을 때만 페이지가 정상적으로 보이게 / User-> 페이지에 접근가능한 사용자를 최고관리자 or 스태프로 제한
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Tag

# 포스트 작성자만 수정할 수 있게 구현
from django.core.exceptions import PermissionDenied

# 태그가 없으면 새로 만들도록
from django.utils.text import slugify

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

# 장고에서 제공하는 CreateView를 상속  
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    # 접근가능한 사용자를 최고관리자 or 스태프
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    # 자동으로 author 필드 채우기(form_valid => 방문자가 폼에 담아 보낸 유효한 정보를 사용해 포스트를 만들고, 이 포스트의 고유 경로로 보내주는 역할)
    def form_valid(self, form):
        currnet_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = currnet_user

            # 태그 출력
            response = super(PostCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
            # return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')

# 장고에서 제공하는 PostUpdate 클래스를 상속(CBV스타일)
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    # 템플릿 파일 지정
    template_name = 'blog/post_update_form.html'

    # dispatch => 방문자가 웹 사이트서버에 Get방식으로 요청했는지 Post 방식으로 요철했는지 판단
    # 권한이 없는 사용자가 postupdate를 사용하려고 하면 통신방식에 상관없이 접근 할 수 없도록 수정
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
            # 권한이 없는 사용자가 포스트를 수정하려 할 때 오류 메세지 출력

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

# tag 페이지(해당 tag만 보여주도록)
def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()


    return render(
        request,
            # post_list와 동일한 출력모양(템플릿 설정)
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag' : tag,
            'categories':Category.objects.all(),
            'no_category_post_count':Post.objects.filter(category=None).count(),
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
