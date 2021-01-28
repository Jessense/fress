from django.urls import path
from django.conf.urls import url, include
from . import views
urlpatterns = [
    path('hello/', views.Hello.as_view()),
    path('crawler/', include('app.crawler.urls')),
]
