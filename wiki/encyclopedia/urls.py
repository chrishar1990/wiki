from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search_entries", views.search_entries, name="search_entries"),
    path("create_page", views.create_page, name="create_page"),
    path("random_page", views.random_page, name="random_page"),
    path("edit/<str:title>", views.edit_page, name="edit_page"),
    path("<str:title>", views.entry_page, name="entry_page"),
    #path("<str:title>", views.error, name="error"),
    
]
