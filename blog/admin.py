from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Category, Tag, Comment

# 관리자 페이지에 Post 모델 등록
admin.site.register(Post, MarkdownxModelAdmin)

# 댓글 작성 페이지
admin.site.register(Comment)

# Category name 필드에 값 입력시 자동으로 slug 생성
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# Tag name 필드에 값 입력시 자동으로 slug 생성
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
