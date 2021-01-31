from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.wiki, name="wiki"),   #see around min 25:00 in the lecture
    path("search/", views.search, name="search")
]
