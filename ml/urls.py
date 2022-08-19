from django.urls import path
from . import views

urlpatterns = [
    #view에서 생성한 inputdata
    path('', views.survival, name='survival'),
    path('mlresult/', views.mlresult, name='mlresult'),
]