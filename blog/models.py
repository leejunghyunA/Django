from django.db import models

# User (장고기본모델)을 사용하기 위해 불러옴 author 필드 구현
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
import os


# tag 모델 만들기(unique=True=> 동일한 이름을 갖는건 추가 안함/ SlugField=> 사람이 읽을 수 있는 텍스트로 고유 URL을 만들 때 주사용)
class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    # tag 고유 url 생성
    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

# Category 모델 만들기(unique=True=> 동일한 이름을 갖는건 추가 안함/ SlugField=> 사람이 읽을 수 있는 텍스트로 고유 URL을 만들 때 주사용)
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    # category 고유 url 생성
    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    # Categorys 를 Categories 로 변경 (복수형 직접 설정)
    class Meta:
        verbose_name_plural = 'Categories'

# CharField = 문자를 담는 필드/ TextFied = 문자열의 길이 제한이 없음/ DateTimeField = 월,일,시,분,초를 기록할 수 있게 해주는 필드
class Post(models.Model):
    title = models.CharField(max_length=30)
    # content = models.TextField()
    content = MarkdownxField()

    # 포스트 요약문보여주기
    hook_text = models.CharField(max_length = 100, blank = True)

     # update이미지 저장할 폴더의 경로 규칙 지정
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to = 'blog/files/%Y/%m/%d/', blank=True)

    # <자동으로 작성시간과 수정시간 저장>
    # created_at = 처음으로 레코드가 생성될 때 현재 시각으로 자동저장
    # updated_at = 수정해 다시 저장 할 때마다 그 시각이 저장되도록 해줌 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    # user을 불러와 author 필드 구현(on_delete=models.CASCADE=>포스트 작성자가 데이터베이스에서 삭제되었을 때 포스트도 같이 삭제함)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # 연결된 Category가 삭제된 경우 포스트의 해당 Category 만 삭제되도록 지정(null)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    # 연결된 tag (on_delete 설정은 x=> 연결된 태그가 삭제되면 해당 포스트의 tag필드가 알아서 빈칸으로 바뀌기 때문)
    tags = models.ManyToManyField(Tag, blank=True)

    # 관리자 페이지에서 Post 목록에 title제목과 번호 출력되도록 해줌 self.pk-해당포스트의 pk 값, self.title-해당 포스트의 title값
    # pk는 장고의 모델에 기본적으로 생성되는 필드 = 각 레코드의 고유값 (like 인덱스 번호와 비슷)
    def __str__(self):
        return f'[{self.pk}]{self.title} <작성자-{self.author}>'

    # url 생성규칙 정의(함수정의) - post에 history 버튼 옆에 <VIEW ON SITE> 버튼 생성
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'


    # 파일명 출력
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    # 확장자 
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

    # 마크다운
    def get_content_markdown(self):
        return markdown(self.content)

# comment 댓글 기능
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'

    # 아바타
    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'http://placehold.it/50x50'
    
    