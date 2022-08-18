from django.urls import path
from . import views

urlpatterns = [
    #view에서 생성한 inputdata
    path('', views.inputdata, name='inputdata'),
    path('result/', views.result, name='result'),
]