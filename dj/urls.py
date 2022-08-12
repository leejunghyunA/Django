
# from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

# 표지판 역할 blog/, admin/으로 접속하는 경우

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('', include('single_pages.urls')),
    path('markdownx/', include('markdownx.urls')),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
