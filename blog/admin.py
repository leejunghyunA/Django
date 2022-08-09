from django.contrib import admin
from .models import Post, Category

# 관리자 페이지에 Post 모델 등록
admin.site.register(Post)

# Category name 필드에 값 입력시 자동으로 slug 생성
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
