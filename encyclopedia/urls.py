from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("create", views.create, name="create"),
    path("search", views.search, name="search"),
    path("randoms", views.randoms, name="randoms"),
    path("<str:title>", views.entry, name="entry")
]
