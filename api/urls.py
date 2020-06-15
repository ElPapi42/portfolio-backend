from django.urls import path

from api import views

urlpatterns = [
    path('contribs/', views.GithubContribs.as_view(), name='api-contribs'),
]