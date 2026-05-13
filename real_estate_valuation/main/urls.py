from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('input', views.input, name='input'),
    # path('list_sport/<str:vid_sporta>/', views.list_sport, name='list_sport')
]