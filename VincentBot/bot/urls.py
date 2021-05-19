from django.urls import path
from django.contrib import admin
from . import views

app_name = 'bot'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('callback/', views.callback, name='callback'),
]
