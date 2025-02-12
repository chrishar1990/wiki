from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search_entries", views.search_entries, name="search_entries"),
    path("<str:title>", views.entry_page, name="entry_page"),
    #path("<str:title>", views.error, name="error"),
    
]
