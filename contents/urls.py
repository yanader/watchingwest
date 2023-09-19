from django.urls import path

from contents import views

urlpatterns = [
    path("", views.contents, name="contents"),
]